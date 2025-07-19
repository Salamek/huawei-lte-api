#!/usr/bin/env python3

"""
Exemple de code pour obtenir la liste des appareils filtrés ainsi que l'état du filtre.

Exemples :
  # Récupérer la liste des appareils filtrés et l'état du filtre
  python3 get_filtered_devices.py http://192.168.8.1/ --username admin --password PASSWORD
"""

from argparse import ArgumentParser
from huawei_lte_api.Connection import Connection
from huawei_lte_api.api.WLan import WLan

parser = ArgumentParser()
parser.add_argument('url', type=str)
parser.add_argument('--username', type=str)
parser.add_argument('--password', type=str)
args = parser.parse_args()

with Connection(args.url, username=args.username, password=args.password) as connection:
    wlan = WLan(connection)

    # Obtenir l'état du filtre
    filter_status = wlan.get_filter_status()
    print("Filter Status: {}".format(filter_status))

    # Obtenir la liste des appareils filtrés
    filtered_devices = wlan.get_filtered_devices()
    print("Filtered Devices:")
    for device in filtered_devices:
        print(device)
