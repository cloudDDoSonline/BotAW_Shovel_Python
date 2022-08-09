from datetime import datetime, timezone, timedelta
import time
from logger import log, _log
import logging
import requests
import functools
from eosapi import NodeException, TransactionException, EosApiException, Transaction
from nonce import Nonce, generate_nonce
from eosapi import EosApi
from typing import List, Dict, Union, Tuple
import random
from settings import user_param, interval
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context
import tenacity
from tenacity import wait_fixed, RetryCallState, retry_if_not_exception_type
from requests import RequestException
from dataclasses import dataclass


class CipherAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers='DEFAULT:@SECLEVEL=2')
        kwargs['ssl_context'] = context
        return super(CipherAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context(ciphers='DEFAULT:@SECLEVEL=2')
        kwargs['ssl_context'] = context
        return super(CipherAdapter, self).proxy_manager_for(*args, **kwargs)


class StopException(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)



@dataclass
class HttpProxy:
    proxy: str
    user_name: str = None
    password: str = None

    def to_proxies(self) -> Dict:
        if self.user_name and self.password:
            proxies = {
                "http": "http://{0}:{1}@{2}".format(self.user_name, self.password, self.proxy),
                "https": "http://{0}:{1}@{2}".format(self.user_name, self.password, self.proxy),
            }
        else:
            proxies = {
                "http": "http://{0}".format(self.proxy),
                "https": "http://{0}".format(self.proxy),
            }
        return proxies

class Alien:
    # alien_host = "https://aw-guard.yeomen.ai"

    def __init__(self, wax_account: str, token: str, charge_time: int, proxy: HttpProxy = None):
        self.wax_account: str = wax_account
        self.token: str = token
        self.log: logging.LoggerAdapter = logging.LoggerAdapter(_log, {"tag": self.wax_account})
        self.http = requests.Session()
        self.http.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, " \
                                          "like Gecko) Chrome/101.0.4951.54 Safari/537.36 "
        self.http.trust_env = False
        self.http.request = functools.partial(self.http.request, timeout=60)
        self.http.mount('https://public-wax-on.wax.io', CipherAdapter())
        self.rpc_host = user_param.rpc_domain
        self.eosapi = EosApi(self.rpc_host, timeout=60)
        if user_param.cpu_account and user_param.cpu_key:
            self.eosapi.set_cpu_payer(user_param.cpu_account, user_param.cpu_key)

        if proxy:
            proxies = proxy.to_proxies()
            self.http.proxies = proxies
            self.eosapi.session.proxies = proxies

        retry = tenacity.retry(retry = retry_if_not_exception_type(StopException), wait=self.wait_retry, reraise=False)
        self.mine = retry(self.mine)
        self.query_last_mine = retry(self.query_last_mine)

        self.charge_time: int = charge_time
        self.next_mine_time: datetime = None

        self.trx_error_count = 0

    def wait_retry(self, retry_state: RetryCallState) -> float:
        exp = retry_state.outcome.exception()
        wait_seconds = interval.transact
        if isinstance(exp, RequestException):
            self.log.info("Network Error: {0}".format(exp))
            wait_seconds = interval.net_error
        elif isinstance(exp, NodeException):
            self.log.info((str(exp)))
            self.log.info("Node error, status code【{0}】".format(exp.resp.status_code))
            wait_seconds = interval.transact
        elif isinstance(exp, TransactionException):
            self.trx_error_count += 1
            self.log.info("Transaction failed: {0}".format(exp.resp.text))
            if "is greater than the maximum billable" in exp.resp.text:
                self.log.error("Insufficient CPU resources, may need to stake more WAX, try again later [{0}]".format(self.trx_error_count))
                wait_seconds = interval.cpu_insufficient
            elif "is not less than the maximum billable CPU time" in exp.resp.text:
                self.log.error("Transactions are restricted and may be blocked by the node [{0}]".format(self.trx_error_count))
                wait_seconds = interval.transact
            elif "NOTHING_TO_MINE" in exp.resp.text:
                self.log.error("Account may be blocked, please check manually ERR::NOTHING_TO_MINE")
                raise StopException("Account may be blocked")
        else:
            if exp:
                self.log.info("General error: {0}".format(exp), exc_info=exp)
            else:
                self.log.info("General error")
        if self.trx_error_count >= interval.max_trx_error:
            self.log.info("Transactions keep going wrong [{0}] times, in order to avoid being blocked by the node and the script is stopped, please manually check the problem or replace the node".format(self.trx_error_count))
            raise StopException("Transactions keep going wrong")
        self.log.info("Retry no.{0} in seconds: [{1}]".format(wait_seconds, retry_state.attempt_number))
        return float(wait_seconds)


    def get_table_rows(self, table: str):
        post_data = {
            "json": True,
            "code": "m.federation",
            "scope": "m.federation",
            "table": table,
            "lower_bound": self.wax_account,
            "upper_bound": self.wax_account,
            "index_position": 1,
            "key_type": "",
            "limit": 10,
            "reverse": False,
            "show_payer": False
        }
        return self.eosapi.get_table_rows(post_data)

    # mining
    def mine(self) -> bool:
        # Query the information of the last mining
        last_mine_time, last_mine_tx = self.query_last_mine()

        ready_mine_time = last_mine_time + timedelta(seconds=self.charge_time)
        if datetime.now() < ready_mine_time:
            interval_seconds = self.charge_time + random.randint(user_param.delay1, user_param.delay2)
            self.next_mine_time = last_mine_time + timedelta(seconds=interval_seconds)
            self.log.info("Time is not enough, next mining time: {0}".format(self.next_mine_time))
            return False

        time.sleep(interval.req)
        self.log.info("Start mining")
        # generate nonce
        nonce = generate_nonce(self.wax_account, last_mine_tx)
        nonce = nonce.random_string

        self.log.info("Generated nonce: {0}".format(nonce))

        # Call the contract, serialize the transaction
        trx = {
            "actions": [{
                "account": "m.federation",
                "name": "mine",
                "authorization": [{
                    "actor": self.wax_account,
                    "permission": "active",
                }],
                "data": {
                    "miner": self.wax_account,
                    "nonce": nonce,
                },
            }]
        }
        trx = self.eosapi.make_transaction(trx)
        serialized_trx = list(trx.pack())

        # Wax cloud wallet signature
        signatures = self.wax_sign(serialized_trx)
        time.sleep(interval.req)
        trx.signatures.extend(signatures)
        self.push_transaction(trx)

        interval_seconds = self.charge_time + random.randint(user_param.delay1, user_param.delay2)
        self.next_mine_time = datetime.now() + timedelta(seconds=interval_seconds)
        self.log.info("Next mining time: {0}".format(self.next_mine_time))
        return True


    def push_transaction(self, trx: Union[Dict, Transaction]):
        self.log.info("start push transaction: {0}".format(trx))
        resp = self.eosapi.push_transaction(trx)
        self.log.info("Successful transaction, transaction_id: [{0}]".format(resp["transaction_id"]))
        self.trx_error_count = 0


    def wax_sign(self, serialized_trx: str) -> List[str]:
        self.log.info("Signing via cloud wallet")
        url = "https://public-wax-on.wax.io/wam/sign"
        post_data = {
            "serializedTransaction": serialized_trx,
            "description": "jwt is insecure",
            "freeBandwidth": False,
            "website": "play.alienworlds.io",
        }
        headers = {"x-access-token": self.token}
        resp = self.http.post(url, json=post_data, headers=headers)
        if resp.status_code != 200:
            self.log.info("Signing failed: {0}".format(resp.text))
            if "Session Token is invalid" in resp.text:
                self.log.info("The token is invalid, please get it again")

                r = requests.get("https://api.telegram.org/bot1911660315:AAHxnLdvtlQ60bmndCCNVPeZI9nOwLfK3Uk/sendMessage?chat_id=-688795568&text=" + str(self.wax_account) + "%20-%20The%20token%20is%20invalid,%20please%20get%20it%20again")
                # print(r.status_code)
                # print(r.headers)
                # print(r.content)  # bytes
                # print(r.text)     # r.content as str
                raise StopException("token invalidation")
            else:
                raise NodeException("wax server error: {0}".format
                                    (resp.text), resp)

        resp = resp.json()
        self.log.info("Signed successfully: {0}".format(resp["signatures"]))
        return resp["signatures"]


    def query_last_mine(self) -> Tuple[datetime, str]:
        self.log.info("Querying last mining information")
        resp = self.get_table_rows("miners")
        resp = resp["rows"][0]
        self.log.info("Last mining information: {0}".format(resp))
        last_mine_time = datetime.fromisoformat(resp["last_mine"])
        last_mine_time = last_mine_time.replace(tzinfo=timezone.utc)
        last_mine_time = last_mine_time.astimezone()
        last_mine_time = last_mine_time.replace(tzinfo=None)
        self.log.info("Last mining time: {0}".format(last_mine_time))
        return last_mine_time, resp["last_mine_tx"]

    def run(self):
        try:
            self.mine()
            while True:
                if datetime.now() > self.next_mine_time:
                    self.mine()
                time.sleep(1)
        except StopException as e:
            self.log.info("Mining stopped")
        except Exception as e:
            self.log.exception("Mining exception: {0}".format(str(e)))


# gio = datetime.now()
# if gio.hour > 21 and gio.hour < 6:
#     self.log.info("Next mining time: not mining time")
# else:
#     self.log.info("Next mining time: OK")