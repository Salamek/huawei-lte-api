# huawei-lte-api
API For huawei LAN/WAN LTE Modems,
you can use this to simply send SMS, get information about your internet usage, signal, and tones of other stuff
PS: it is funny how many stuff you can request from modem/router without any authentication

## Installation

```bash
$ pip install huawei-lte-api
```

## Usage

```python3
from huawei_lte_api.Connection import Connection
from huawei_lte_api.Client import Client
from huawei_lte_api.AuthorizedConnection import AuthorizedConnection

# Currently there are TWO types of connection:
# Connection which accepts only router URL with no authentication useful for unauthorized calls (Wen you dont know a password)
# AuthorizedConnection which accepts router URL, username and password useful for unauthorized and authorized calls
# Just use AuthorizedConnection when you have valid credentials

# connection = Connection('http://192.168.8.1/') I have valid credentials no need for limited access
connection = AuthorizedConnection('http://192.168.8.1/', 'admin', 'MY_SUPER_TRUPER_PASSWORD')
client = Client(connection) # This just siplifies acces to separated API groups, you can use device = Device(connection) if you want

print(client.device.information())
```
Result dict
```python
{'DeviceName': 'B310s-22', 'SerialNumber': 'MY_SERIAL_NUMBER', 'Imei': 'MY_IMEI', 'Imsi': 'MY_IMSI', 'Iccid': 'MY_ICCID', 'Msisdn': None, 'HardwareVersion': 'WL1B310FM03', 'SoftwareVersion': '21.311.06.03.55', 'WebUIVersion': '17.100.09.00.03', 'MacAddress1': 'EHM:MY:MAC', 'MacAddress2': None, 'ProductFamily': 'LTE', 'Classify': 'cpe', 'supportmode': None, 'workmode': 'LTE'}
```