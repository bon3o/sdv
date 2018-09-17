#!/usr/bin/python3
# coding: utf8
import re
from datetime import datetime
from OpenSSL import crypto as c
import json
import sys

conf = open('/etc/nginx/nginx.conf')
t = conf.read()


subj = sys.argv[1]
ssl_path = []
main_conf_path = []
sec_conf_path = []
jsonData = []

ssl_path1 =  re.findall(r"ssl_certificate\s\s*(.*?);", t) #Пути к сертификатам в основном конфиге

for i in ssl_path1:
    ssl_path.append(i)


path =  re.findall("include (\S.*?);\n", t) #Пути к конфигам проектов
path = [s.replace('/etc/nginx/', '') for s in path]

for i in path:
    main_conf_path.append(i)


a=0
for i in main_conf_path:
    loc = '/etc/nginx/' + main_conf_path[a]
    conf = open(loc)
    cf = conf.read()
    ssl_path2 =  re.findall(r"ssl_certificate\s\s*(.*?);", cf) #Пути к сертификатам в конфиге
    for s in ssl_path2:
        ssl_path.append(s)
    sec_path = re.findall("include (.*?);\n", cf) #Пути к конфигам проектов
    for p in sec_path:
        sec_conf_path.append(p)
    a= a+1


sec_conf_path = set(sec_conf_path)
sec_conf_path = list(sec_conf_path)
a=0
for s in sec_conf_path:
    loc = '/etc/nginx/' + sec_conf_path[a]
    conf = open(loc)
    cf = conf.read()
    ssl_path3 =  re.findall(r"ssl_certificate\s\s*(.*?);", cf) #Пути к сертификатам в конфиге
    for s in ssl_path3:
        ssl_path.append(s)
    a = a+1


ssl_path = set(ssl_path)
ssl_path = list(ssl_path)
r = re.compile(".*pem")
ssl_path = filter(r.match, ssl_path)

a=0
for f in ssl_path:
    cert = c.load_certificate(c.FILETYPE_PEM, file('/etc/nginx/' + ssl_path[a]).read())
    date = datetime.strptime(cert.get_notAfter(),"%Y%m%d%H%M%SZ")
    datestr = cert.get_notAfter()
    now = datetime.now()
    duein = date - now  
    domain = cert.get_subject().CN
    jsonData.append({"{#CERT.DOMAIN}": domain, "{#CERT.DUE.IN}": duein.days,
                         "{#CERT.PATH}": '/etc/nginx/' + ssl_path[a]})
    a=a+1


if subj == 'd':
    print(json.dumps({"data": jsonData}, indent=4))  
else:
    for i in jsonData:
        if i['{#CERT.PATH}'] == subj:
            day = i['{#CERT.DUE.IN}'] 
        if day < 0:
            day = 0
            print(day)
        else:
            print(day)

