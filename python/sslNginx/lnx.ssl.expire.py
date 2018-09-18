#!/usr/bin/python
# coding: utf8
import re
import os
from os import listdir
from os.path import isfile, join
from datetime import datetime
from OpenSSL import crypto as c
import json
import sys

jsonData = []

path = sys.argv[1]

if re.search(".*pem", path):
   cert = c.load_certificate(c.FILETYPE_PEM, file(path).read())
   date = datetime.strptime(cert.get_notAfter(),"%Y%m%d%H%M%SZ")
   datestr = cert.get_notAfter()
   now = datetime.now()
   duein = date - now
   due_in = duein.days
   if due_in < 0:
      due_in = 0
   print(due_in)

else: 

   files = [f for f in listdir(path) if isfile(join(path, f))]
   certs = set(files)
   certs = list(files)
   r = re.compile(".*pem")
   certs = filter(r.match, certs)

   for cert in certs:
      certif = c.load_certificate(c.FILETYPE_PEM, file(path+cert).read())
      domain = certif.get_subject().CN
      jsonData.append({"{#CERT.PATH}": path + cert, "{#CERT.DOMAIN}": domain})
   print(json.dumps({"data": jsonData}, indent=4))   