#!/usr/bin/env python3
import json
import os
import subprocess
import urllib.request as Web
import requests
import socket
import zipfile
import tempfile
import shutil
import sys
import getopt
import time

pubK = None
prvK = None


def GenerateWG(path):
    global pubK
    global prvK
    if os.path.isdir(path) != True:
        os.mkdir(path)
    subprocess.check_output(
        f"wg genkey | tee {path}privatekey | wg pubkey > {path}publickey", shell=True).decode("utf-8").strip()
    prvK = open(path + 'privatekey', 'r').readline().rstrip()
    print(f' {colors.UNDERLINE}Private Key : {prvK}{colors.ENDC}')
    pubK = open(path + 'publickey', 'r').readline().rstrip()
    print(f' {colors.UNDERLINE}Public Key : {pubK}{colors.ENDC}')


def Login(user, paswd, config_path):
    if os.path.isdir(config_path) != True:
        os.mkdir(config_path)
    url = "https://api.uymgg1.com/v1/auth/login"
    payload = json.dumps({"username": user, "password": paswd})
    headers = {
        'Host': 'api.uymgg1.com',
        'Content-Type': 'application/json;charset=utf-8',
        'Accept': 'application/json',
        'Accept-Charset': 'utf-8',
        'X-Device-Brand': 'Apple',
        'Ss-Variant-Slugs': 'test_36:b;test_34:a;test_41:b;feature_1:b;test_28:a;feature_chat_apple:b;feature_shadowsocks:b;test_50:a;test_55:b;feature_rotator:a',
        'Accept-Language': 'en-US;q=1.0',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Surfshark/2.24.0 (com.surfshark.vpnclient.ios; build:19; iOS 14.8.1) Alamofire/5.4.3 device/mobile'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.ok:
        print(f'{colors.OKGREEN} Logged In{colors.ENDC}')
        open(config_path + 'config.json', 'w').write(response.text)
    else:
        print(f'{colors.FAIL} Error {response.status_code}{colors.ENDC}')
        exit()


def GetInfo(token):

    url = "https://api.uymgg1.com/v1/payment/subscriptions/current"
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}',
        'Accept-Charset': 'utf-8',
        'Ss-Variant-Slugs': 'test_36:b;test_34:a;test_41:b;feature_1:b;test_28:a;feature_chat_apple:b;feature_shadowsocks:b;test_50:a;test_55:b;feature_rotator:a;test108:b',
        'Accept-Language': 'en-US;q=1.0',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Surfshark/2.24.0 (com.surfshark.vpnclient.ios; build:19; iOS 14.8.1) Alamofire/5.4.3 device/mobile'
    }
    response = requests.request("GET", url, headers=headers)
    if response.ok:
        JS = json.loads(response.text)
        print(
            f"{colors.BOLD} Plan Details{colors.ENDC}\n Plan: {JS['name']}\n End Date: {JS['expiresAt']}")
    else:
        print(f' Error {response.status_code}')
        exit()


def RegisterWireGuard(token, pubkey):

    url = "https://api.uymgg1.com/v1/account/users/public-keys"
    payload = json.dumps({"pubKey": pubkey})
    headers = {
        'Content-Type': 'application/json;charset=utf-8',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}',
        'Accept-Charset': 'utf-8',
        'Ss-Variant-Slugs': 'test_36:b;test_34:a;test_41:b;feature_1:b;test_28:a;feature_chat_apple:b;feature_shadowsocks:b;test_50:a;test_55:b;feature_rotator:a;test108:b',
        'Accept-Language': 'en-US;q=1.0',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Surfshark/2.24.0 (com.surfshark.vpnclient.ios; build:19; iOS 14.8.1) Alamofire/5.4.3 device/mobile'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200 or response.status_code == 201:
        print(
            f" Status: OK\n Register: True\n Valid: {json.loads(response.text)['expiresAt']}")
    else:
        print(f" Error {response.status_code}")
        sys.exit(2)


def Builder(path):
    temp = tempfile.mkdtemp(prefix='wiregen-')
    request = Web.Request('https://api.uymgg1.com/v4/server/clusters/generic')
    request.add_header(
        "user-agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")
    JData = json.loads(Web.urlopen(
        request).read())
    unique = {each['location']: each for each in JData}.values()
    print(f'{colors.OKBLUE} Generating zip file{colors.ENDC}')
    archive = zipfile.ZipFile(
        path+'Wireguard-Confs.zip', 'w', zipfile.ZIP_DEFLATED)
    for i in unique:
        ip = socket.gethostbyname(i['connectionName'])
        with open(temp + '/' + i['location'] + '.conf', 'w') as file:
            wg = f"# Script by Incognito Coder @IC_mods\n[Interface]\nPrivateKey = {prvK}\nAddress = 10.14.0.2/16\nDNS = 162.252.172.57, 149.154.159.92\n\n[Peer]\nPublicKey = {i['pubKey']}\nAllowedIps= 0.0.0.0/0\nEndpoint = {ip}:51820"
            file.write(wg)
            file.close()
            archive.write(temp + '/' + i['location'] +
                          '.conf', i['location'] + '.conf')
            print(
                f"{colors.OKBLUE} {i['location']}{colors.ENDC} Created Successfully.")

    print(f'{colors.OKGREEN} Built{colors.ENDC}')
    shutil.rmtree(temp)


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


path = 'Wireguard-Data/'


def help():

    os.system('cls' if os.name == 'nt' else 'clear')
    print(
        "┌───────────────────────────────────────────────────────────────────────┐\n"
        f"|{colors.OKCYAN}\t ____              __ ____  _                _    {colors.ENDC}\t\t|\n"
        f"|{colors.OKCYAN}\t/ ___| _   _ _ __ / _/ ___|| |__   __ _ _ __| | __{colors.ENDC}\t\t|\n"
        f"|{colors.OKCYAN}\t\___ \| | | | '__| |_\___ \| '_ \ / _` | '__| |/ /{colors.ENDC}\t\t|\n"
        f"|{colors.OKCYAN}\t ___) | |_| | |  |  _|___) | | | | (_| | |  |   < {colors.ENDC}\t\t|\n"
        f"|{colors.OKCYAN}\t|____/ \__,_|_|  |_| |____/|_| |_|\__,_|_|  |_|\_\ {colors.ENDC}\t\t| \n"
        f"|{colors.FAIL}\t__        _____ ____  _____ ____ _   _   _    ____  ____  {colors.ENDC}\t|\n"
        f"|{colors.FAIL}\t\ \      / /_ _|  _ \| ____/ ___| | | | / \  |  _ \|  _ \ {colors.ENDC}\t|\n"
        f"|{colors.FAIL}\t \ \ /\ / / | || |_) |  _|| |  _| | | |/ _ \ | |_) | | | |{colors.ENDC}\t|\n"
        f"|{colors.FAIL}\t  \ V  V /  | ||  _ <| |__| |_| | |_| / ___ \|  _ <| |_| |{colors.ENDC}\t|\n"
        f"|{colors.FAIL}\t   \_/\_/  |___|_| \_\_____\____|\___/_/   \_\_| \_\____/ {colors.ENDC}\t|\n"
        "|\t\t\t\t\t\t\t\t\t|\n"
        "├───────────────────────────────────────────────────────────────────────┤\n"
        "|\t\t\t\t\t\t\t\t\t|\n"
        f"|{colors.WARNING}\t Developer : Incognito Coder || Channel : T.me/IC_MODS   {colors.ENDC}\t|\n"
        "|\t\t\t\t\t\t\t\t\t|\n"
        "├───────────────────────────────────────────────────────────────────────┤\n"
        "| Version : 2.3 || GitHub : https://github.com/Incognito-Coder/Wiregen  |\n"
        "└───────────────────────────────────────────────────────────────────────┘"
    )
    print(f'{colors.HEADER}'
          '[1] Create Configs\n'
          '[2] Exit App'
          f'{colors.ENDC}')
    opt = input('> ')
    if opt == '1':
        email = input(f'{colors.BOLD} Enter Account Email : {colors.ENDC}')
        password = input(
            f'{colors.BOLD} Enter Account Password : {colors.ENDC}')
        Login(email, password, path)
        GenerateWG(path)
        jayson = json.load(open(f'{path}config.json'))
        GetInfo(jayson['token'])
        RegisterWireGuard(jayson['token'], pubK)
        Builder(path)
    elif opt == '2':
        sys.exit(0)
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Undefined option.Exiting ...')
        time.sleep(2)


def main(argv):
    short_args = 'hu:p:'
    long_args = ['help', 'user=', 'pass=']
    username = ''
    password = ''
    try:
        opts, args = getopt.getopt(argv, short_args, long_args)
    except getopt.GetoptError:
        sys.exit(2)
    if argv:
        for opt, arg in opts:
            if opt in ('-u', '--user'):
                username = arg
            elif opt in ('-p', '--pass'):
                password = arg
            elif opt in ("-h", "--help"):
                print(f'Incognito Coder SurfShark Wireguard Generator\n'
                      'Usage : -u TEXT -p TEXT')
                sys.exit(0)
        Login(username, password, path)
        GenerateWG(path)
        jayson = json.load(open(f'{path}config.json'))
        RegisterWireGuard(jayson['token'], pubK)
        Builder(path)
    else:
        print('No argument passed!')
        help()


if __name__ == "__main__":
    main(sys.argv[1:])
