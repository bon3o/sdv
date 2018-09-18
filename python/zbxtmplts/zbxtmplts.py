#!/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
import os
import xml.dom.minidom
from datetime import datetime
from sys import exit
from pyzabbix import ZabbixAPI
from requests.packages.urllib3.exceptions import InsecureRequestWarning


Zabbix_Host = 'http://10.20.0.10/'
Zabbix_User = 'api-user'
Zabbix_Password = 'zabbix_password'
dir_path = '/backup/ZBXTemplatesExport'


def get_time():
    get_time = datetime.fromtimestamp(int(time.mktime(datetime.now().timetuple()))).strftime('%Y-%m-%dT%H:%M:%SZ')
    return get_time

def get_timestamp():
    get_timestamp = datetime.fromtimestamp(int(time.mktime(datetime.now().timetuple()))).strftime('%Y-%m-%d_%H:%M:%S')
    return get_timestamp


def login_to_zabbix():
    Connection_Timeout = 25
    zapi = ZabbixAPI(Zabbix_Host, timeout=Connection_Timeout)
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    zapi.login(Zabbix_User, Zabbix_Password)
    zapi.session.auth = (Zabbix_User, Zabbix_Password)
    zapi.timeout = Connection_Timeout
    return zapi

def get_templates():
    templates = []
    zapi = login_to_zabbix()
    Get_Templates = zapi.template.get(output=['templateid', 'name'])
    for template in Get_Templates:
        templates.append(template)
    return templates

def export_templates():
    zapi = login_to_zabbix()
    templates = get_templates()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    for template in templates:
        template_id = template['templateid']
        template_name = template['name']
        template_name = template_name.replace("/", "|")
        timestamp = get_timestamp()
        rules = {
            "options": {
                "templates": [template_id]
                },
            "format": "xml"
         }
        nm = template_name
        template_name_out = dir_path + '/' + template_name + '_' + timestamp + '.xml'
        result = zapi.do_request('configuration.export', rules)
        template = xml.dom.minidom.parseString(result['result'].encode('utf-8'))
        date = template.getElementsByTagName("date")[0]
        now_time = get_time()
        date.firstChild.replaceWholeText(now_time)
        try:
            f = open(template_name_out, 'wb')
            f.write(template.toprettyxml().encode('utf-8'))
            f.close()
            print nm,
            print ' - Ok'
        except Exception:
            print nm,
            print (' I cant write to file: ', Exception)

    return export_templates


def main():
    Start_Time = time.time()

    zapi = login_to_zabbix()
    export = export_templates()

if __name__ == '__main__':
    main()
