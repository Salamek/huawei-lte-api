#!/usr/bin/env python3

"""
Exemple de code pour ajouter des adresses MAC à votre liste de blocage.

Exemples :
  # Ajouter une seule adresse MAC
  python3 mac_filter.py http://192.168.8.1/ --username admin --password PASSWORD --mac 66:77:88:99:AA:BB --hostname device_name --status 2

  # Ajouter plusieurs adresses MAC
  python3 mac_filter.py http://192.168.8.1/ --username admin --password PASSWORD --mac 66:77:88:99:AA:BB 11:22:33:44:55:66 --hostname device1 device2 --status 2
"""

from argparse import ArgumentParser
from huawei_lte_api.Connection import Connection
from huawei_lte_api.api.WLan import WLan


parser = ArgumentParser()
parser.add_argument('url', type=str)
parser.add_argument('--username', type=str)
parser.add_argument('--password', type=str)
parser.add_argument('--mac', type=str, nargs='+', help='Une ou plusieurs adresses MAC à filtrer')
parser.add_argument('--hostname', type=str, nargs='+', help='Nom(s) d\'hôte correspondant aux adresses MAC')
parser.add_argument('--index', type=str, default='0', help="Indice du SSID (par défaut : 0)")
parser.add_argument('--status', type=str, help='État du filtre (1=liste blanche, 2=liste noire)')
args = parser.parse_args()

# Vérifier que nous avons le même nombre de MAC et de noms d\'hôte
if len(args.mac) != len(args.hostname):
    raise ValueError("The number of MAC addresses and hostnames must be the same")

with Connection(args.url, username=args.username, password=args.password) as connection:
    wlan = WLan(connection)

    # Utiliser la nouvelle fonction d\'aide au lieu de créer le dictionnaire à la main
    response = wlan.filter_mac_addresses(
        mac_list=args.mac,
        hostname_list=args.hostname,
        ssid_index=args.index,
        filter_status=args.status
    )
    print("Response: {}".format(response))
