#!/usr/bin/env python3

"""
Example code on how to receive basic info about your router, you can try it by running:
python3 device_info.py http://admin:PASSWORD@192.168.8.1/
"""

from argparse import ArgumentParser

from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection

parser = ArgumentParser()
parser.add_argument("url", type=str)
parser.add_argument("--username", type=str)
parser.add_argument("--password", type=str)
args = parser.parse_args()

with Connection(args.url, username=args.username, password=args.password) as connection:
    client = Client(connection)
    print(client.device.information())
