#!/usr/bin/env python3

"""
Example code on how to create dialup profile, you can try it by running:
python3 connect_with_proxy.py http://admin:PASSWORD@192.168.8.1/ name
"""
from argparse import ArgumentParser

from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection

parser = ArgumentParser()
parser.add_argument("url", type=str)
parser.add_argument("name", type=str)
parser.add_argument("--username", type=str)
parser.add_argument("--password", type=str)
args = parser.parse_args()

with Connection(
        args.url,
        username=args.username,
        password=args.password,
) as connection:
    client = Client(connection)
    print(client.dial_up.create_profile(args.name))
