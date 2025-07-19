#!/usr/bin/env python3
"""
Exemple de code pour reconnecter la connexion :
python3 reconnect_dialup.py http://admin:PASSWORD@192.168.8.1/
"""
from argparse import ArgumentParser
from huawei_lte_api.Connection import Connection
from huawei_lte_api.Client import Client
from huawei_lte_api.enums.client import ResponseEnum


parser = ArgumentParser()
parser.add_argument('url', type=str)
parser.add_argument('--username', type=str)
parser.add_argument('--password', type=str)
args = parser.parse_args()

with Connection(args.url, username=args.username, password=args.password) as connection:
    client = Client(connection)
    print('Disabling dialup...')
    if client.dial_up.set_mobile_dataswitch(0) == ResponseEnum.OK.value:
        print('OK')
    else:
        print('Error')
    print('Enabling dialup...')
    if client.dial_up.set_mobile_dataswitch(1) == ResponseEnum.OK.value:
        print('OK')
    else:
        print('Error')


