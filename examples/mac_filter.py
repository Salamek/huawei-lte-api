#!/usr/bin/env python3

"""
Example code To add a Mac address to your blocklist, you can try it by running:
python3 mac_filter.py http://192.168.8.1/ --username admin --password PASSWORD --mac 66:77:88:99:AA:BB --hostname fake_mac_adr --index 0 --status 2
"""

from argparse import ArgumentParser
from huawei_lte_api.Connection import Connection
from huawei_lte_api.api.WLan import WLan


parser = ArgumentParser()
parser.add_argument('url', type=str)
parser.add_argument('--username', type=str)
parser.add_argument('--password', type=str)
parser.add_argument('--mac', type=str)
parser.add_argument('--hostname', type=str)
parser.add_argument('--index', type=str)
parser.add_argument('--status', type=str)
args = parser.parse_args()
args = parser.parse_args()

with Connection(args.url, username=args.username, password=args.password) as connection:
    wlan = WLan(connection)
    clients = [{'WifiMacFilterMac0': args.mac,
                'wifihostname0': args.hostname, 'Index': args.index, 'WifiMacFilterStatus': args.status}]
    response = wlan.set_multi_macfilter_settings(clients)
