#!/usr/bin/python
# coding: utf8
import os
import sys
import configparser


service_name = sys.argv[1]


def check_status(service_name):
    status = os.system('systemctl status ' + service_name + ' > /dev/null')
    return status


def start_service(service_name):
    os.system('systemctl start ' + service_name + ' > /dev/null')


if __name__ == '__main__':
    if check_status(service_name):
        start_service(service_name)

