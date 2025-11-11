#!/usr/bin/env python3

"""
Display 4G/5G modem signal strength using vertical bars and show operator + access mode.
Example usage:
python3 signal_bars.py http://admin:PASSWORD@192.168.8.1/
"""

from __future__ import annotations

import re
from argparse import ArgumentParser

from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection

SIGNAL_LEVELS = {
    0: "     ",
    1: "▂    ",
    2: "▂▃   ",
    3: "▂▃▄  ",
    4: "▂▃▄▅ ",
    5: "▂▃▄▅▇",
}


def parse_dbm(value: str | None) -> int | None:
    if value is None:
        return None
    match = re.search(r"-?\d+", value)
    return int(match.group()) if match else None


def get_signal_level(rsrp: int | None) -> int:
    if rsrp is None:
        return 0
    if rsrp >= -80:
        return 5
    if rsrp >= -90:
        return 4
    if rsrp >= -100:
        return 3
    if rsrp >= -110:
        return 2
    if rsrp >= -120:
        return 1
    return 0


def generate_signal_bars(level: int, total: int = 5) -> str:
    """
    Create a vertical bar chart (like a phone signal icon).
    Each bar grows higher from left to right.
    """
    result = []
    for row in range(total, 0, -1):
        line = ""
        for col in range(1, total + 1):
            if col <= level and row <= col:
                line += "▇ "
            else:
                line += "  "
        result.append(line.rstrip())
    return "\n".join(result)


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("url", type=str)
    parser.add_argument("--username", type=str)
    parser.add_argument("--password", type=str)
    args = parser.parse_args()

    with Connection(args.url, username=args.username, password=args.password) as connection:
        client = Client(connection)

        # Get signal and network info
        signal_info = client.device.signal()
        status_info = client.monitoring.status()
        network_type_raw = str(status_info.get("CurrentNetworkType", "0"))

        network_type_map = {
            "0": "No Service",
            "1": "GSM",
            "2": "GPRS",
            "3": "EDGE",
            "4": "WCDMA",
            "5": "HSDPA",
            "6": "HSUPA",
            "7": "HSPA",
            "8": "TDSCDMA",
            "9": "HSPA+",
            "10": "EVDO Rev.0",
            "11": "EVDO Rev.A",
            "12": "EVDO Rev.B",
            "13": "1xRTT",
            "14": "UMB",
            "15": "1xEVDV",
            "16": "3xRTT",
            "17": "HSPA+ 64QAM",
            "18": "HSPA+ MIMO",
            "19": "LTE",
            "41": "LTE CA",
            "101": "NR5G NSA",
            "102": "NR5G SA",
        }
        plmn_info = client.net.current_plmn()

        # Parse and determine values
        rsrp = parse_dbm(signal_info.get("rsrp"))
        rsrq = signal_info.get("rsrq")
        sinr = signal_info.get("sinr")

        level = get_signal_level(rsrp)
        bars = SIGNAL_LEVELS[level]

        operator_name = plmn_info.get("FullName") or plmn_info.get("ShortName") or "Unknown"

        # Map internal mode codes (if any) to readable labels
        mode_map = {
            "LTE": "4G",
            "WCDMA": "3G",
            "GSM": "2G",
            "NR5G": "5G",
            "NR": "5G",
        }
        readable_mode = network_type_map.get(network_type_raw, f"Unknown ({network_type_raw})")
        if readable_mode in mode_map:
            readable_mode = mode_map[readable_mode]

        # Get IP address
        config = client.config_lan.config()
        modem_ip = config["config"]["dhcps"]["ipaddress"]

        # Display
        print(f"{operator_name} {readable_mode} {bars}")

        print(f"  RSRP: {signal_info.get('rsrp')}")
        if rsrq:
            print(f"  RSRQ: {rsrq}")
        if sinr:
            print(f"  SINR: {sinr}")
        print(f"  IP: {modem_ip}")


if __name__ == "__main__":
    main()
