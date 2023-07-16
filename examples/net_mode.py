#!/usr/bin/env python3

"""
Example code for how to set the network mode and the LTE bands:

python3 net_mode.py http://admin:PASSWORD@192.168.8.1/ --mode 4g --lteband 3 --lteband 7 --primary-lteband 7
python3 net_mode.py http://admin:PASSWORD@192.168.8.1/ --mode auto --lteband all

This script tries to avoid changing any settings if the router config already matches.
"""

import sys
from argparse import ArgumentParser
from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection
from huawei_lte_api.enums.net import LTEBandEnum, NetworkModeEnum

MODES = {
    'auto': NetworkModeEnum.MODE_AUTO,
    '2g': NetworkModeEnum.MODE_2G_ONLY,
    '3g': NetworkModeEnum.MODE_3G_ONLY,
    '3g2g': NetworkModeEnum.MODE_3G_2G_AUTO,
    '4g': NetworkModeEnum.MODE_4G_ONLY,
    '4g2g': NetworkModeEnum.MODE_4G_2G_AUTO,
    '4g3g': NetworkModeEnum.MODE_4G_3G_AUTO,
}

BANDS = {
    'all': LTEBandEnum.ALL,
    '1': LTEBandEnum.B1,
    '3': LTEBandEnum.B3,
    '7': LTEBandEnum.B7,
    '8': LTEBandEnum.B8,
    '20': LTEBandEnum.B20,
    '28': LTEBandEnum.B28,
    '38': LTEBandEnum.B38,
    '40': LTEBandEnum.B40,
}

parser = ArgumentParser()
parser.add_argument('url', type=str)
parser.add_argument('--username', type=str)
parser.add_argument('--password', type=str)
parser.add_argument('--primary-lteband', type=str, choices=BANDS.keys(),
                    help="the primary LTE band, e.g. '7'")
parser.add_argument('--lteband', type=str, action='append', choices=BANDS.keys(),
                    help="additional LTE bands, can be set multiple times to add more bands")
parser.add_argument('--mode', type=str, choices=MODES.keys())
args = parser.parse_args()

with Connection(args.url, username=args.username, password=args.password) as connection:
    client = Client(connection)

    print("Querying current network configuration...")
    orig_net_mode = client.net.net_mode()

    # Do we need to change the network mode?
    needs_mode = False
    if args.mode is not None and orig_net_mode['NetworkMode'] != MODES[args.mode].value:
        needs_mode = True

    # Do we need to change the primary LTE band?
    needs_primary_lteband = False
    if args.primary_lteband is not None:
        signal = client.device.signal()
        needs_primary_lteband = signal['band'] != args.primary_lteband and args.primary_lteband != 'all'

    # Do we need to change the LTE bands in general?
    needs_lteband = False
    bands = set()
    if args.lteband is not None:
        bands.update(args.lteband)
    if args.primary_lteband is not None:
        bands.add(args.primary_lteband)
    needed_band = 0
    for band in bands:
        needed_band |= BANDS[band]
    if len(bands) and orig_net_mode['LTEBand'] != hex(needed_band)[2:]:
        needs_lteband = True
        # XXX: if we set the bands to "all" we get back a different LTEBand value covering
        # all supported bands and not the "All Bands" one, so if the value is in the band
        # list assume we are already in "all" mode and don't need to do anything
        if needed_band == LTEBandEnum.ALL:
            net_mode_list = client.net.net_mode_list()
            band_list_values = set(e["Value"].lower() for e in net_mode_list['LTEBandList']['LTEBand'])
            if orig_net_mode['LTEBand'].lower() in band_list_values:
                needs_lteband = False

    if not needs_mode and not needs_primary_lteband and not needs_lteband:
        print("Configuration matches, nothing to do")
        sys.exit()

    new_network_lteband = hex(needed_band)[2:] if needs_lteband else orig_net_mode['LTEBand']
    new_network_band = orig_net_mode['NetworkBand']
    new_network_mode = MODES[args.mode].value if needs_mode else orig_net_mode['NetworkMode']

    if needs_primary_lteband:
        # The only way I found to change the primary LTE band with CA is to set it alone,
        # wait, and then add the second band. Note that the primary band isn't fixed
        # and the router can jump to another one on its own and you need to run
        # this again to revert it.
        primary_lteband = BANDS[args.primary_lteband]
        print("Setting primary LTE band to %s..." % args.primary_lteband)
        client.net.set_net_mode(primary_lteband, new_network_band, new_network_mode)
        print("Waiting for primary LTE band to change to %s..." % args.primary_lteband)
        while True:
            signal = client.device.signal()
            if signal['band'] == args.primary_lteband:
                break
        needs_mode = False
        needs_lteband = len(bands) > 1

    if needs_lteband:
        print("Setting LTE bands to %s..." % bands)
        client.net.set_net_mode(new_network_lteband, new_network_band, new_network_mode)
        needs_mode = False

    if needs_mode:
        print("Setting network mode to %s..." % args.mode)
        client.net.set_net_mode(new_network_lteband, new_network_band, new_network_mode)

    print("Done")
