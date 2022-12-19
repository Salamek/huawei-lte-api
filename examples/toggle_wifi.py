#!/usr/bin/env python3
"""
Example code on how to send a SMS, you can try it by running:
python3 send_sms.py http://admin:PASSWORD@192.168.8.1/ +420123456789 "Hello world"
"""
from argparse import ArgumentParser
from huawei_lte_api.Connection import Connection
from huawei_lte_api.Client import Client
from huawei_lte_api.enums.client import ResponseEnum


parser = ArgumentParser()
parser.add_argument('url', type=str)
parser.add_argument('enabled', type=bool)
parser.add_argument('--username', type=str)
parser.add_argument('--password', type=str)
args = parser.parse_args()

with Connection(args.url, username=args.username, password=args.password) as connection:
    client = Client(connection)
    if client.wlan.wifi_network_switch(args.enabled) == ResponseEnum.OK.value:
        print('Wi-Fi was toggled successfully')
    else:
        print('Error')
