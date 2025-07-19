#!/usr/bin/env python3

"""
Exemple de code pour récupérer les informations de base de votre routeur. Vous pouvez essayer en exécutant :
python3 device_info.py http://admin:PASSWORD@192.168.8.1/
"""

from argparse import ArgumentParser
from huawei_lte_api.Connection import Connection
from huawei_lte_api.Client import Client


parser = ArgumentParser()
parser.add_argument('url', type=str)
parser.add_argument('--username', type=str)
parser.add_argument('--password', type=str)
args = parser.parse_args()

with Connection(args.url, username=args.username, password=args.password) as connection:
    client = Client(connection)
    print(client.device.information())
