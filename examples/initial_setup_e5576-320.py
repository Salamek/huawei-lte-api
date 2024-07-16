from argparse import ArgumentParser

from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection
from time import sleep

parser = ArgumentParser()
parser.add_argument('--password', type=str)
parser.add_argument('--new-password', type=str)
parser.add_argument('--ssid', type=str)
parser.add_argument('--wpa-password', type=str)
args = parser.parse_args()

original_password = args["password"]
new_password = args["new-password"]

wifi_ssid = args["ssid"]
wifi_password = args["wpa-password"]

url = 'http://192.168.8.1/'
with Connection(url, password=original_password) as connection:
    client = Client(connection)

    locale = "en-us"
    print("Set language to " + locale)
    print(client.language.set_current_language(locale))

    print("Accept privacy policy")
    print(client.app.accept_privacypolicy(approve=True))

    print("Set autoupdate config")
    print(client.online_update.set_autoupdate_config(autoupdate=True))

    print("Set basic information")
    print(client.device.set_basic_information())

    print(f"Set wlan ({wifi_ssid}/{wifi_password}) and account settings (admin/{new_password})")
    resp = client.wlan.set_wlan_guide_settings(
        ssid=wifi_ssid, wpa_psk=wifi_password, current_password=original_password, new_password=new_password
    )
    print(resp)

print("Admin password changed, reconnect...")
sleep(10)
failing = True
while failing:
    try:
        with Connection(url, password=new_password) as connection:
            print("Get basic information")
            status = client.monitoring.status()
            if status["ConnectionStatus"] == "901":
                failing = False
            else:
                sleep(60)
    except Exception as e:
        print("Failed with exception: " + str(e) + ", sleeping 60s")
        sleep(60)

with Connection(url, password=new_password) as connection:
    client = Client(connection)

    print("Set basic information")
    print(client.device.set_basic_information())

    # restart wifi to see effect of the new ssid
    # see toggle_wifi.py



