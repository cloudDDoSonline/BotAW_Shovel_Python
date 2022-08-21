import logger
from logger import log
import ruamel.yaml
yaml = ruamel.yaml.YAML()
from ruamel.yaml.comments import CommentedMap
from settings import user_param, load_param
from alien import Alien, HttpProxy
import traceback
import sys
import ctypes
import requests


def start():
    user_yml = "user.yml"
    if len(sys.argv) == 2:
        user_yml = sys.argv[1]

    with open(user_yml, "r", encoding="utf8") as file:
        data: CommentedMap = yaml.load(file)
        file.close()
    load_param(data)

    logger.init_loger(user_param.account)

    if user_param.note:
        cmdtitle = user_param.note + ". " + user_param.account
    else:
        cmdtitle = user_param.account
   
    ctypes.windll.kernel32.SetConsoleTitleW(cmdtitle)
    proxy = None
    if user_param.proxy:
        proxy = HttpProxy(user_param.proxy, user_param.proxy_username, user_param.proxy_password)

    log.info("Loading configuration file: {0}".format(user_yml))
    log.info("=============Start mining=============")
    alien = Alien(user_param.account, user_param.token, user_param.charge_time, proxy, user_param.note, user_param.telegram_id)
    alien.run()
    log.info("=============Mining stopped=============")



def main():
    print(r"""     _____  ____  ____  _  _        __    __    ____  ____  _  _ 
    (  _  )(  _ \( ___)( \( )      /__\  (  )  (_  _)( ___)( \( )
     )(_)(  )___/ )__)  )  (      /(  )\  )(__  _)(_  )__)  )  ( 
    (_____)(__)  (____)(_)\_)    (__)(__)(____)(____)(____)(_)\_)""")
    print("  ****************************************************************")
    print("  * OpenAlien Open source v1.0.2                                 *")
    print("  * Project address: https://github.com/encoderlee/OpenAlien     *")
    print("  * English version by ThienCNTT - https://github.com/thiencntt  *")
    print("  ****************************************************************")                       

    # r = requests.get("https://api.telegram.org/bot1911660315:AAHxnLdvtlQ60bmndCCNVPeZI9nOwLfK3Uk/sendMessage?chat_id=-688795568&text=bot%20python%20alien%20ok")

    # print(r.status_code)
    # print(r.headers)
    # print(r.content)  # bytes
    # print(r.text)     # r.content as str

    try:
        start()
    except Exception as e:
        traceback.print_exc()
    input("Press enter to exit")


if __name__ == '__main__':
    main()

