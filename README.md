# OpenAlien
![version](https://img.shields.io/badge/version-1.0.2-blue)
![license](https://img.shields.io/badge/license-MIT-brightgreen)
![python_version](https://img.shields.io/badge/python-%3E%3D%203.10-brightgreen)
![coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
[![](https://img.shields.io/badge/blog-@thiencntt.com-red)](https://thiencntt.com)
### A free and open source Alien Worlds bot
![](https://raw.githubusercontent.com/thiencntt/botawpython/main/doc/demo.png)
## Illustrate
Alien Worlds official website: [https://alienworlds.io](https://alienworlds.io)

Original source code: [https://github.com/encoderlee/OpenAlien](https://github.com/encoderlee/OpenAlien)

You can get a free and open source FarmersWorld bot:
[https://github.com/encoderlee/OpenFarmer](https://github.com/encoderlee/OpenFarmer)

This open source OpenAlien completely runs without using the Chrome browser.

This script can run multiple account in one computer

# Usage

1. To run from source code, install the Python environment first. It is recommended to install Python 3.9.13 version, because this is the version we have tested

download link：[https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe](https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe)

Remember to check when installing “Add Python 3.9 to PATH”

2. Download the source code and click the green button on the github project page【Code】,【Download ZIP】, after downloading, unzip it

3. Double click to run【install_dependencies.bat】Install the dependency package, this step only needs to be done once per computer

【Notice】Before installing the dependency package, please close other windows and downloading applications

4. Open file 【user - sample.txt】to know what to fill in file【user.bat】

5. Make a copy of file【user.bat】and fill information of another account

### Configuration file description

```yaml
#Note that there is a space after the colon of each parameter name, do not lose the space when modifying the parameters

# Wax node address, using public nodes, sometimes the network is blocked, or access is restricted too frequently, 429 errors occur, you can change nodes, or build private nodes
# List of public nodes：https://wax.eosio.online/endpoints

rpc_domain: https://wax.pink.gg

# cpu payment number, cpu_key fill in the private key of the payment number, leave it blank if no payment is required
cpu_account:
cpu_key:

# Even if the mining time is up, delay the mining for 30-90 seconds
delay1: 30
delay2: 90

# http proxy (eg 127.0.0.1:10808)
# Set an HTTP proxy for the script, which can solve the problem of restricted access to public nodes to a certain extent, leave it blank if it is not needed
proxy:
proxy_username:
proxy_password:

# Change the following three items to your account information
# account is the account name of the wax cloud wallet
# What is the token, first log in to the WAX cloud wallet manually in the chrome browser  https://wallet.wax.io/dashboard
# Then enter the address in the chrome browser to navigate to： https://all-access.wax.io/api/session
# Copy the token and fill it below
# Note that after copying the token from the Chrome browser, the browser can click the fork in the upper right corner to close, but do not click to log out of the account, and do not directly log in to another account, otherwise the previous account will be disconnected.
# If you need to log in to a second account in Chrome, use Chrome's multi-profile feature to log in


# charge_time is the mining interval, in seconds, log in to the official website of alienworlds, open the tool page, you can see it, fill in according to the actual situation

account: gts3c.c.wam
token: EHuyFHPcLpSNUJ4BLSUnPxxxxxxxxxxxx
charge_time: 336

```

### Common Errors
1. Transaction error

There are many reasons for transaction errors, such as smart contract errors, insufficient CPU, wrong keys, WAX node restrictions, etc.

If there are 5 transaction errors in a row, the script will stop. At this time, you need to manually check the problem or replace the node

Why not just keep trying again and again? Because of repeatedly submitting wrong transactions, the public node will block you, and it will take 24 hours before you can use the node

Setting up your own WAX private node will improve this problem to a certain extent

2. Node error

Node errors, especially 429 errors, are mainly because you have too many numbers running at the same time under one IP, frequent requests, and are blocked by the node

After all, public nodes are free services for the world. In order to prevent abuse, many restrictions have been made.

Setting a proxy IP for every N number, or setting up WAX private nodes by yourself, will improve this problem to a certain extent

### Donate

Wax wallet address of encoderlee: m45yy.wam

Wax wallet address of thiencntt: focvu.wam