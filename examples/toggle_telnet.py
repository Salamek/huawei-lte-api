#!/usr/bin/env python3
"""
Example code on how to enable/disable telnet (tested on B310-22):
python3 toggle_telnet.py http://admin:PASSWORD@192.168.8.1/ 1
python3 toggle_telnet.py http://admin:PASSWORD@192.168.8.1/ 0
Telnet is usually open on port 23
"""
from argparse import ArgumentParser

from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection
from huawei_lte_api.enums.client import ResponseEnum
from huawei_lte_api.enums.device import ModeEnum

parser = ArgumentParser()
parser.add_argument("url", type=str)
parser.add_argument("enabled", type=bool)
parser.add_argument("--username", type=str)
parser.add_argument("--password", type=str)
args = parser.parse_args()

with Connection(args.url, username=args.username, password=args.password) as connection:
    client = Client(connection)
    if client.device.mode(ModeEnum.ENABLE_TELNET if args.enabled else ModeEnum.NORMAL) == ResponseEnum.OK.value:
        print("Telnet enabled successfully")
    else:
        print("Error")
