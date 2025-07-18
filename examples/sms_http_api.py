#!/usr/bin/env python3
"""
Expose a simple HTTP API for sending SMS messages.

Example usage:
python3 sms_http_api.py http://192.168.8.1/ \
    --username admin --password PASSWORD \
    --host 0.0.0.0 --port 8000
# Then send SMS with curl:
# curl -X POST -H "Content-Type: application/json" \
#      -d '{"to": ["+420123456789"], "text": "Hello"}' http://0.0.0.0:8000/sms
"""

from argparse import ArgumentParser
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from huawei_lte_api.Connection import Connection
from huawei_lte_api.Client import Client
from huawei_lte_api.enums.client import ResponseEnum


class SMSHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/sms':
            self.send_error(404, 'Not found')
            return

        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        try:
            data = json.loads(body.decode('utf-8'))
            recipients = data['to']
            text = data['text']
            if not isinstance(recipients, list) or not isinstance(text, str):
                raise ValueError
        except (ValueError, KeyError, json.JSONDecodeError):
            self.send_error(400, 'Invalid JSON body')
            return

        try:
            with Connection(self.server.modem_url, username=self.server.username,
                            password=self.server.password) as connection:
                client = Client(connection)
                resp = client.sms.send_sms(recipients, text)
            if resp == ResponseEnum.OK.value:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'OK')
            else:
                self.send_error(500, 'Failed to send SMS')
        except Exception as exc:
            self.send_error(500, str(exc))


class SMSHTTPServer(HTTPServer):
    def __init__(self, server_address, handler_class, modem_url, username, password):
        super().__init__(server_address, handler_class)
        self.modem_url = modem_url
        self.username = username
        self.password = password


def main():
    parser = ArgumentParser()
    parser.add_argument('url', type=str)
    parser.add_argument('--username', type=str)
    parser.add_argument('--password', type=str)
    parser.add_argument('--host', type=str, default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()

    server = SMSHTTPServer((args.host, args.port), SMSHandler, args.url,
                           args.username, args.password)
    print(f'Serving on {args.host}:{args.port}')
    server.serve_forever()


if __name__ == '__main__':
    main()
