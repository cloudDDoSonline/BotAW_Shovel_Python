@echo off
echo rpc_domain: https://api.wax.alohaeos.com> user.yml
echo cpu_account: xxxxxxxxxxxx>> user.yml
echo cpu_key: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx>> user.yml
echo delay1: 30>> user.yml
echo delay2: 90>> user.yml
echo proxy:>> user.yml
echo proxy_username:>> user.yml
echo proxy_password:>> user.yml
echo telegram_id:>> user.yml
echo note:>> user.yml
echo account: xxxxx.wam>> user.yml
echo token: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx>> user.yml
echo charge_time: xxx>> user.yml
python main.py user.yml
