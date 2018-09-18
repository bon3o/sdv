#!/usr/bin/python3
# coding: utf8
import requests
import json
import configparser
import sys

"""
Запускаем скрипт с двумя обязательными параметрами ЛОГИН и ПАРОЛЬ от морды Акамая

./akadns.py login password

На выходе получаем "0", если искомая строка найдена, либо "1", если нет.
"""


config = configparser.ConfigParser()
lgn = sys.argv[1]
pwd = sys.argv[2]
url = 'https://control.akamai.com/ids-authn-login/v2/verification/'
url2 = 'https://control.akamai.com/portal/adns.jsp?sidebar=FastDNS_configuration&tab=CONFIGURE&type=context&gid=32628'
OurString = 'To add a new active zone or zones' # Искомая строка


data = {
    'password': pwd,
    'userIdentifier': lgn
}


headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'Host': 'control.akamai.com',
    'Referer': 'https://control.akamai.com/apps/auth/?TARGET_URL=Y29udHJvbC5ha2FtYWkuY29tL2hvbWVuZy92aWV3L21haW4='
}


def check():
    r = requests.session()
    r.post(url, data=json.dumps(data), headers=headers)
    response = r.get(url2)
    result = str.find(response.text, OurString)

    if result > 0:
        res = 0
    else:
        res = 1
    return res


try:
    aka = check()
    print(aka)


except:
    print(1)
