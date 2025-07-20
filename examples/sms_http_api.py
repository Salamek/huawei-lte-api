#!/usr/bin/env python3
"""

Expose une API HTTP simple pour envoyer des SMS.

Exemple d'utilisation :
python3 sms_http_api.py http://192.168.8.1/ \
    --username admin --password PASSWORD \
    --host 0.0.0.0 --port 80
# Puis envoyez un SMS avec curl :
# curl -X POST -H "Content-Type: application/json" \
#      -d '{"to": ["+420123456789"], "from": "+420987654321", "text": "Hello"}' http://0.0.0.0:80/sms
Chaque requête est également enregistrée dans une base SQLite. Le chemin de cette base peut
être défini avec l'option ``--db`` ou la variable d'environnement ``SMS_API_DB``.
Par défaut, ``sms_api.db`` est utilisé.

"""

from argparse import ArgumentParser
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

import os
import re
import sqlite3
from datetime import datetime
import urllib.parse


from huawei_lte_api.Connection import Connection
from huawei_lte_api.Client import Client
from huawei_lte_api.enums.client import ResponseEnum


SIGNAL_LEVELS = {
    0: "     ",
    1: "▂    ",
    2: "▂▃   ",
    3: "▂▃▄  ",
    4: "▂▃▄▅ ",
    5: "▂▃▄▅▇",
}

NETWORK_TYPE_MAP = {
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


def parse_dbm(value):
    if value is None:
        return None
    match = re.search(r"-?\d+", str(value))
    return int(match.group()) if match else None


def get_signal_level(rsrp: int) -> int:
    if rsrp is None:
        return 0
    if rsrp >= -80:
        return 5
    elif rsrp >= -90:
        return 4
    elif rsrp >= -100:
        return 3
    elif rsrp >= -110:
        return 2
    elif rsrp >= -120:
        return 1
    else:
        return 0


def ensure_logs_table(conn):
    conn.execute(
        "CREATE TABLE IF NOT EXISTS logs ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "timestamp TEXT,"
        "phone TEXT,"
        "sender TEXT,"
        "message TEXT,"
        "response TEXT)"
    )
    cols = [row[1] for row in conn.execute("PRAGMA table_info(logs)")]
    if "sender" not in cols:
        conn.execute("ALTER TABLE logs ADD COLUMN sender TEXT")


def log_request(db_path, recipients, sender, text, response):
    conn = sqlite3.connect(db_path)
    ensure_logs_table(conn)
    conn.execute(
        "INSERT INTO logs(timestamp, phone, sender, message, response) VALUES (?,?,?,?,?)",
        (datetime.utcnow().isoformat(), ",".join(recipients), sender, text, response),
    )
    conn.commit()
    conn.close()



def validate_request(data):
    """Validate JSON payload and return sanitized fields."""
    recipients = data.get("to")
    sender = data.get("from")
    text = data.get("text")

    if isinstance(sender, str):
        sender = sender.strip()

    if not isinstance(recipients, list) or not recipients:
        raise ValueError("'to' must be a non-empty list")
    for number in recipients:
        if not isinstance(number, str) or not re.fullmatch(r"\+?\d+", number):
            raise ValueError("invalid phone number in 'to'")
    if not isinstance(sender, str) or not sender:
        raise ValueError("'from' must be a non-empty string")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("'text' must be a non-empty string")
    return recipients, sender, text.strip()


# Elements d'interface communs
NAVBAR = """
    <nav class='navbar navbar-dark bg-company'>
      <div class='container-fluid'>
        <button class='navbar-toggler' type='button' data-bs-toggle='offcanvas' data-bs-target='#menu' aria-controls='menu'>
          <span class='navbar-toggler-icon'></span>
        </button>
        <span class='navbar-brand ms-2'>API SMS BC</span>
      </div>
    </nav>
    <div class='offcanvas offcanvas-start' tabindex='-1' id='menu'>
      <div class='offcanvas-header'>
        <h5 class='offcanvas-title'>Menu</h5>
        <button type='button' class='btn-close' data-bs-dismiss='offcanvas' aria-label='Close'></button>
      </div>
      <div class='offcanvas-body'>
        <ul class='nav flex-column'>
          <li class='nav-item'><a class='nav-link' href='/'>Accueil</a></li>
          <li class='nav-item'><a class='nav-link' href='/logs'>Historique SMS</a></li>
          <li class='nav-item'><a class='nav-link' href='/testsms'>Envoyer un SMS</a></li>
        </ul>
      </div>
    </div>
"""



class SMSHandler(BaseHTTPRequestHandler):
    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json_error(self, status, message):
        self._send_json(status, {"error": message})

    def do_GET(self):

        if self.path == "/":
            self._serve_index()
            return
        if self.path == "/logs":
            self._serve_logs()
            return
        if self.path == "/testsms":
            self._serve_testsms()
            return
        if self.path != "/health":
            self.send_error(404, "Not found")

            return

        try:
            with Connection(
                self.server.modem_url,
                username=self.server.username,
                password=self.server.password,
            ) as connection:
                client = Client(connection)
                device_info = client.device.information()
                signal_info = client.device.signal()
                status_info = client.monitoring.status()
                network_type_raw = str(status_info.get("CurrentNetworkType", "0"))
                plmn_info = client.net.current_plmn()
                config = client.config_lan.config()

            rsrp = parse_dbm(signal_info.get("rsrp"))
            level = get_signal_level(rsrp)

            health = {
                "device_info": device_info,
                "signal": signal_info,
                "operator_name": plmn_info.get("FullName")
                or plmn_info.get("ShortName")
                or "Unknown",
                "network_type": NETWORK_TYPE_MAP.get(
                    network_type_raw, f"Unknown ({network_type_raw})"
                ),
                "ip_address": config.get("config", {})
                .get("dhcps", {})
                .get("ipaddress"),
                "signal_level": level,
                "signal_bars": SIGNAL_LEVELS.get(level),
            }

            body = json.dumps(health).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except Exception as exc:
            self._json_error(500, str(exc))

    def _serve_index(self):
        html = """
        <html>
        <head>
            <meta charset='utf-8'>
            <title>Modem Health</title>
            <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css'>
            <script src='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js'></script>
            <style>
                .bg-company {background-color:#0060ac;}
                .btn-company {background-color:#0060ac;border-color:#0060ac;}
            </style>
            <script>
                async function loadHealth() {
                    const r = await fetch('/health');
                    const data = await r.json();
                    document.getElementById('health').textContent = JSON.stringify(data, null, 2);
                }
                window.onload = loadHealth;
            </script>
        </head>
        <body class='container py-4'>
            {NAVBAR}
            <h1 class='mb-3'>Informations du modem</h1>
            <pre id='health' class='bg-light p-3 rounded'>Chargement...</pre>
        </body>
        </html>
        """.replace("{NAVBAR}", NAVBAR)
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_logs(self):
        conn = sqlite3.connect(self.server.db_path)
        conn.row_factory = sqlite3.Row
        ensure_logs_table(conn)
        rows = conn.execute(
            "SELECT id, timestamp, sender, phone, message, response FROM logs ORDER BY id DESC"
        ).fetchall()
        conn.close()

        html = [
            "<html><head><meta charset='utf-8'><title>Historique SMS</title>",
            "<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css'>",
            "<script src='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js'></script>",
            "<style>.bg-company{background-color:#0060ac;}.btn-company{background-color:#0060ac;border-color:#0060ac;}</style>",
            "<script>function selectAll(){document.querySelectorAll('.rowchk').forEach(c=>c.checked=true);}</script>",
            "</head><body class='container py-4'>",
            NAVBAR,
            "<h1 class='mb-3'>Historique des SMS</h1>",
            "<form method='post' action='/logs/delete'>",
            "<table class='table table-striped'>",
            "<tr><th></th><th>Date/Heure</th><th>Expéditeur</th><th>Destinataire(s)</th><th>Message</th><th>Réponse</th></tr>",
        ]
        for row in rows:
            html.append(
                f"<tr><td><input type='checkbox' class='rowchk' name='ids' value='{row['id']}'></td><td>{row['timestamp']}</td><td>{row['sender'] or ''}</td><td>{row['phone']}</td><td>{row['message']}</td><td>{row['response']}</td></tr>"
            )
        html.extend(
            [
                "</table>",
                "<p><button type='button' class='btn btn-secondary me-2' onclick='selectAll()'>Sélectionner tout</button> <button type='submit' class='btn btn-danger'>Supprimer</button></p>",
                "</form>",
                "<p><a href='/' class='btn btn-link'>Retour</a></p></body></html>",
            ]
        )
        body = "".join(html).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_testsms(self):
        html = """
        <html>
        <head>
            <meta charset='utf-8'>
            <title>Envoyer un SMS</title>
            <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css'>
            <script src='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js'></script>
            <style>
                .bg-company {background-color:#0060ac;}
                .btn-company {background-color:#0060ac;border-color:#0060ac;}
            </style>
            <script>
                async function sendSms(event) {
                    event.preventDefault();
                    const to = document.getElementById('to').value
                        .split(',')
                        .map(t => t.trim())
                        .filter(t => t);
                    const text = document.getElementById('text').value;
                    const payload = {to: to, from: 'test api web', text: text};
                    const resp = await fetch('/sms', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(payload)
                    });
                    if (resp.ok) {
                        alert('SMS envoyé');
                    } else {
                        const msg = await resp.text();
                        alert('Erreur: ' + msg);
                    }
                }
            </script>
        </head>
        <body class='container py-4'>
            {NAVBAR}
            <h1 class='mb-3'>Tester l\'envoi de SMS</h1>
            <form id='smsForm' onsubmit='sendSms(event)' class='mb-3'>
                <div class='mb-3'>
                    <label for='to' class='form-label'>Destinataire(s) (séparés par des virgules)</label>
                    <input type='text' id='to' class='form-control' required>
                </div>
                <div class='mb-3'>
                    <label for='text' class='form-label'>Message</label>
                    <textarea id='text' class='form-control' rows='4' required></textarea>
                </div>
                <button type='submit' class='btn btn-company'>Envoyer</button>
            </form>
            <p><a href='/' class='btn btn-link'>Retour</a></p>
        </body>
        </html>
        """.replace("{NAVBAR}", NAVBAR)
        body = html.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _delete_logs(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        params = urllib.parse.parse_qs(body)
        ids = params.get("ids", [])
        conn = sqlite3.connect(self.server.db_path)
        conn.row_factory = sqlite3.Row
        ensure_logs_table(conn)
        if ids:
            placeholders = ",".join("?" for _ in ids)
            conn.execute(f"DELETE FROM logs WHERE id IN ({placeholders})", ids)
            conn.commit()
        conn.close()
        self.send_response(303)
        self.send_header("Location", "/logs")
        self.end_headers()


    def do_POST(self):
        if self.path == "/logs/delete":
            self._delete_logs()
            return
        if self.path != "/sms":

            self._json_error(404, "Not found")

            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        try:
            data = json.loads(body.decode("utf-8"))

        except json.JSONDecodeError:
            self._json_error(400, "Invalid JSON body")
            return

        try:
            recipients, sender, text = validate_request(data)
        except ValueError as exc:
            self._json_error(400, str(exc))

            return

        try:

            with Connection(
                self.server.modem_url,
                username=self.server.username,
                password=self.server.password,
            ) as connection:
                client = Client(connection)
                resp = client.sms.send_sms(recipients, text)
            log_request(self.server.db_path, recipients, sender, text, str(resp))

            if resp == ResponseEnum.OK.value:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"OK")
            else:

                self._json_error(500, "Failed to send SMS")

        except Exception as exc:

            log_request(self.server.db_path, recipients, sender, text, str(exc))

            self._json_error(500, str(exc))


class SMSHTTPServer(HTTPServer):
    def __init__(
        self, server_address, handler_class, modem_url, username, password, db_path
    ):

        super().__init__(server_address, handler_class)
        self.modem_url = modem_url
        self.username = username
        self.password = password
        self.db_path = db_path


def main():
    parser = ArgumentParser()
    parser.add_argument("url", type=str)
    parser.add_argument("--username", type=str)
    parser.add_argument("--password", type=str)
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=80)
    parser.add_argument("--db", type=str, default=os.getenv("SMS_API_DB", "sms_api.db"))

    args = parser.parse_args()

    server = SMSHTTPServer(
        (args.host, args.port),
        SMSHandler,
        args.url,
        args.username,
        args.password,
        args.db,
    )

    print(f"Serving on {args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
