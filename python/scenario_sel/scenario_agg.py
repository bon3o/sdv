#!/usr/bin/python3
# coding: utf8
from pyzabbix import ZabbixAPI, ZabbixAPIException
import sys
import json

zbxurl = 'http://monitoring'
zbxname = 'api-scripts'
zbxpass = '99iFdurfck2323'
z = ZabbixAPI(zbxurl)
z.login(zbxname, zbxpass)

groupname = sys.argv[1]
param = sys.argv[2]
step = sys.argv[3] if len(sys.argv) >= 4 else 'none'

def list():
    groups = z.hostgroup.get(output=['itemid', 'name'])

    for i in groups:
        if i['name'] == groupname:
            groupid = i['groupid']

    hosts = z.host.get(groupids=groupid, output=['hostid', 'name'])
    host = hosts[0]
    hid = host['hostid']
    items = z.item.get(hostids=hid, output=['hostid', 'name'])
    jsonData = []

    for i in items:
        s = i['name']
        r = s.find('Result')
        if r > 0:
            jsonData.append({"{#STEP.AGG.NAME}": s})
    print(json.dumps({"data": jsonData}, indent=4))


def count():
    groups = z.hostgroup.get(output=['itemid', 'name'])
    for i in groups:
        if i['name'] == groupname:
            groupid = i['groupid']


    hosts = z.host.get(groupids=groupid, output=['hostid', 'name'])
    cnt = len(hosts)
    print(cnt)


def check():
    groups = z.hostgroup.get(output=['itemid', 'name'])
    for i in groups:
        if i['name'] == groupname:
            groupid = i['groupid']
    failcount = 0
    hosts = z.host.get(groupids=groupid, output=['hostid', 'name'])
    c = 0
    for h in hosts:
        host = hosts[c]
        c += 1
        hid = host['hostid']
        items = z.item.get(hostids=hid, output=['hostid', 'name', 'lastvalue'])
        for i in items:
            if i['name'] == step:
                res = i['lastvalue']
                res = int(res)
                if res == 0:
                    failcount += 1
    print(failcount)


if param == 'list':
    list()
if param == 'count':
    count()
if param == 'check':
    check()
