#!/usr/bin/python3
# coding: utf8
import sys
import os
import subprocess
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import requests
import configparser
import json
import warnings
warnings.filterwarnings("ignore")
config = configparser.ConfigParser()
param = sys.argv[1]
cfgfile = sys.argv[2]
stepname = sys.argv[3] if len(sys.argv) >= 4 else 'none'

def login():
    loginInId = config[Step]['loginInId']
    passInId = config[Step]['passInId']
    login = config[Step]['login']
    pwd = config[Step]['pass']
    logBtn = config[Step]['logBtn']
    username = driver.find_element_by_id(loginInId)
    password = driver.find_element_by_id(passInId)
    username.send_keys(login)
    password.send_keys(pwd)
    driver.find_element_by_name(logBtn).click()

def select():
    element_id = config[Step]['element_id']
    value = config[Step]['value']
    select = select = Select(driver.find_element_by_id(element_id))
    select.select_by_value(value)

def test():
    try:
       response = requests.get(url)
       status_code = response.status_code
       load_time = response.elapsed.total_seconds()
       driver.get(url)
       if need_auth > 0:
          login()
       if need_select > 0:
          select()
       html = driver.page_source
       result = str.find(html, stpstring)
       if result > 0:
           step_result = 1
       else:
           step_result = 0
           driver.save_screenshot(cfgfile + "." + Step + '.png')
        #jsonData.append({"{#SCENARIO.STEP}": i, "{#RESPONSE.CODE}": status_code, "{#LOAD.TIME}": load_time, "{#KEY.WORDS}": stpstring, "{#STEP.NAME}": stpname})
       resultlist.append("[" + config[Step]['name'] + "]")
       resultlist.append("Result = " + str(step_result))
       resultlist.append("StatusCode = " + str(status_code))
       resultlist.append("LoadTime = " + str(load_time))
       resultlist.append("KeyWords = " + str(stpstring))
    except Exception:
       resultlist.append("[" + config[Step]['name'] + "]")
       resultlist.append("Result = 0")


if param == "list":
   l = 1
   config.read(cfgfile)
   num = int(config['NOS']['nos'])
   jsonData = []
   while l <= num:
       d = str(l)
       lStep = "Step" + d
       lstpname = config[lStep]['name']
       jsonData.append({"{#SCENARIO.STEP}": l,"{#STEP.NAME}": lstpname})
       l += 1
   print(json.dumps({"data": jsonData}, indent=4))

if param == "test":
   try:
      resultlist = []
      i = 1
      config.read(cfgfile)
      num = int(config['NOS']['nos'])
      driver = webdriver.PhantomJS(service_log_path=os.path.devnull)

      while i <= num:
         c = str(i)
         Step = "Step" + c
         url = config[Step]['url']
         need_auth = int(config[Step]['need_auth'])
         need_select = int(config[Step]['need_select'])
         stpstring = config[Step]['string']
         stpname = config[Step]['name']
         test()
         i += 1

      with open(cfgfile + ".log", 'w') as log:
         log.write("\n".join(resultlist))
      log.close()
      driver.quit()
   except Exception:
      log.close()
      driver.quit()

if param == "result":
    logfile =  cfgfile + "." + "log"
    config.read(logfile)
    print(config[stepname]['Result'])


if param == "status":
    logfile =  cfgfile + "." + "log"
    config.read(logfile)
    print(config[stepname]['StatusCode'])


if param == "time":
    logfile =  cfgfile + "." + "log"
    config.read(logfile)
    print(config[stepname]['LoadTime'])
