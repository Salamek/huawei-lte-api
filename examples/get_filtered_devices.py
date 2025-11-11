#!/usr/bin/env python3

"""
Example code to get the list of filtered devices and the filter status.

Examples:
  # Get the list of filtered devices and the filter status
  python3 get_filtered_devices.py http://192.168.8.1/ --username admin --password PASSWORD
"""

from argparse import ArgumentParser

from huawei_lte_api.api.WLan import WLan
from huawei_lte_api.Connection import Connection

parser = ArgumentParser()
parser.add_argument("url", type=str)
parser.add_argument("--username", type=str)
parser.add_argument("--password", type=str)
args = parser.parse_args()

with Connection(args.url, username=args.username, password=args.password) as connection:
    wlan = WLan(connection)

    # Get the filter status
    filter_status = wlan.get_filter_status()
    print(f"Filter Status: {filter_status}")

    # Get the list of filtered devices
    filtered_devices = wlan.get_filtered_devices()
    print("Filtered Devices:")
    for device in filtered_devices:
        print(device)
