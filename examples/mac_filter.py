#!/usr/bin/env python3

"""
Example code to add MAC addresses to your blocklist.

Examples:
  # Add a single MAC address
  python3 mac_filter.py http://192.168.8.1/ --username admin --password PASSWORD --mac 66:77:88:99:AA:BB --hostname device_name --status 2

  # Add multiple MAC addresses
  python3 mac_filter.py http://192.168.8.1/ --username admin --password PASSWORD --mac 66:77:88:99:AA:BB 11:22:33:44:55:66 --hostname device1 device2 --status 2
"""

from argparse import ArgumentParser

from huawei_lte_api.api.WLan import WLan
from huawei_lte_api.Connection import Connection

parser = ArgumentParser()
parser.add_argument("url", type=str)
parser.add_argument("--username", type=str)
parser.add_argument("--password", type=str)
parser.add_argument("--mac", type=str, nargs="+", help="One or more MAC addresses to filter")
parser.add_argument("--hostname", type=str, nargs="+", help="Hostnames corresponding to MAC addresses")
parser.add_argument("--index", type=str, default="0", help="Index for the SSID (default: 0)")
parser.add_argument("--status", type=str, help="Filter status (1=whitelist, 2=blacklist)")
args = parser.parse_args()

# Validate that we have the same number of MACs and hostnames
if len(args.mac) != len(args.hostname):
    raise ValueError("The number of MAC addresses and hostnames must be the same")

with Connection(args.url, username=args.username, password=args.password) as connection:
    wlan = WLan(connection)

    # Use the new helper function instead of manually creating the dictionary
    response = wlan.filter_mac_addresses(
        mac_list=args.mac,
        hostname_list=args.hostname,
        ssid_index=args.index,
        filter_status=args.status,
    )
    print(f"Response: {response}")
