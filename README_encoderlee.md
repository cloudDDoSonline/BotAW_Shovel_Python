# OpenAlien
![version](https://img.shields.io/badge/version-1.0.2-blue)
![license](https://img.shields.io/badge/license-MIT-brightgreen)
![python_version](https://img.shields.io/badge/python-%3E%3D%203.6-brightgreen)
![coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
[![](https://img.shields.io/badge/blog-@encoderlee-red)](https://encoderlee.blog.csdn.net)
### A free and open source Alien Worlds automated hang-up contract script
![](https://raw.githubusercontent.com/encoderlee/OpenAlien/main/doc/demo1.png)
## Illustrate
Alien Worlds official website: [https://alienworlds.io](https://alienworlds.io)

We have launched a free and open source FarmersWorld contract script before:
[https://github.com/encoderlee/OpenFarmer](https://github.com/encoderlee/OpenFarmer)

This time, the contract script of Alien Worlds is launched:
[https://github.com/encoderlee/OpenAlien](https://github.com/encoderlee/OpenAlien)

Old users understand, no need to say more

Compared with the previous OpenFarmer, this open source OpenAlien completely runs away from the Chrome browser.

The underlying EOSIO SDK consists of the original [【eospy】](https://github.com/eosnewyork/eospy) Replaced by our own development [【eosapi】](https://github.com/encoderlee/eosapi) ，
Improved stability and the number of multiple openings on a single computer

Welcome to my blog: [https://encoderlee.blog.csdn.net](https://encoderlee.blog.csdn.net)

### Welcome to join our QQ group to communicate and discuss：568229631

# Usage

### video tutorial：

[https://www.bilibili.com/video/BV1da4115757](https://www.bilibili.com/video/BV1da4115757)

[https://www.youtube.com/watch?v=hZSl-2QyJys](https://www.youtube.com/watch?v=hZSl-2QyJys)

### How to use (method 1)：

Directly click the link below to download the latest packaged version (or find it in [Releases] on the right side of the github page). The packaged version only supports Win10 or higher operating systems.

[【click here to download】](https://github.com/encoderlee/OpenAlien/releases/download/1.0.2/OpenAlien_1.0.2.zip)

Unzip the files in the compressed package, first modify the configuration file【user.yml】, and then double-click to run【user.bat】

Open a second account, copy【user.yml】to【user2.yml】，copy【user.bat】to【user2.bat】

Modify the configuration file【user2.yml】and enter information of the second account，modify【user2.bat】file, put the string inside “user.yml” change to “user2.yml”，Then double click to run【user2.bat】

Open more accounts, and so on

### How to use (method 2)：

1.To run from source code, install the Python environment first. It is recommended to install Python 3.9.13 version, because this is the version we have tested

download link：[https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe](https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe)

Remember to check when installing “Add Python 3.9 to PATH”

2.Download the source code and click the green button on the github project page【Code】,【Download ZIP】, after downloading, unzip it

3.Double click to run【install_dependencies.bat】Install the dependency package, this step only needs to be done once per computer

【Notice】Before installing the dependency package, please close the agent such as Ladder to avoid downloading errors

4.Modify the configuration file first【user.yml】，Double click to run【user.bat】

5.The multi-opening method is the same as above, that is, copy these two files, modify them and run

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
# charge_time is the mining interval, in seconds, log in to the official website of alienworlds, open the tool page, you can see it, fill in according to the actual situation

account: gts3c.c.wam
token: EHuyFHPcLpSNUJ4BLSUnPxxxxxxxxxxxx
charge_time: 336

```





List of public nodes：[https://wax.eosio.online/endpoints](https://wax.eosio.online/endpoints)

Note that after copying the token from the Chrome browser, the browser can click the fork in the upper right corner to close, but do not click to log out of the account, and do not directly log in to another account, otherwise the previous account will be disconnected.

If you need to log in to a second account in Chrome, use Chrome's multi-user feature to log in

Chrome multiuser related articles：[https://www.chensnotes.com/chrome-profile.html](https://www.chensnotes.com/chrome-profile.html)

### Common tools

Use【Visual Studio Code】[https://code.visualstudio.com/download](https://code.visualstudio.com/download) or 【nodepad++】[https://notepad-plus-plus.org/downloads/v8.4.2](https://notepad-plus-plus.org/downloads/v8.4.2) to edit files
【user.yml】

【cmder】[https://cmder.net](https://cmder.net)

Replace the cmd command line tool that comes with windows to prevent the script from suspended animation

The cmd command line tool that comes with the system, the quick editing mode is turned on by default, sometimes due to the accidental operation of the mouse and keyboard,

The log will stay in one place, in a state of suspended animation, causing the script to not run continuously. Use【cmder】to solve the problem


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

### Welcome to reward

Wax wallet address:

m45yy.wam
