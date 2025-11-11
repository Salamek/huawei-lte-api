#!/usr/bin/env python3

"""
Reads received SMS
Example usage:
python3 read_sms.py http://admin:PASSWORD@192.168.8.1/
"""

from argparse import ArgumentParser

from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("url", type=str)
    parser.add_argument("--username", type=str)
    parser.add_argument("--password", type=str)
    args = parser.parse_args()

    with Connection(args.url, username=args.username, password=args.password) as connection:
        client = Client(connection)

        # Lire tous les SMS
        sms_messages = client.sms.get_sms_list()

        messages = sms_messages.get("Messages", {}).get("Message", [])
        for message in messages:
            print(f"Index: {message['Index']}")
            print(f"From: {message['Phone']}")
            print(f"Content: {message['Content']}")
            print(f"Date: {message['Date']}")
            print("-" * 20)
        print("No received SMS found.")


if __name__ == "__main__":
    main()
