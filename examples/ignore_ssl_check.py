#!/usr/bin/env python3

"""
Example code on how to ignore SSL checks to accept expired or self signed SSL certs, you can try it by running:
python3 ignore_ssl_check.py http://admin:PASSWORD@192.168.8.1/
"""
from argparse import ArgumentParser

import requests

from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection

parser = ArgumentParser()
parser.add_argument("url", type=str)
parser.add_argument("--username", type=str)
parser.add_argument("--password", type=str)
args = parser.parse_args()


# Create custom requests.Session
my_custom_session = requests.Session()
# Disable SSL verify
my_custom_session.verify = False

with my_custom_session, Connection(
        args.url,
        username=args.username,
        password=args.password,
        requests_session=my_custom_session,
) as connection:
    client = Client(connection)
    print(client.device.information())
