# huawei-lte-api
API For huawei LAN/WAN LTE Modems,
you can use this to simply send SMS, get information about your internet usage, signal, and tons of other stuff

Tested on:
* Huawei B310s-22
* Huawei B525s-23a
* Huawei E5186s-22a

PS: it is funny how many stuff you can request from modem/router without any authentication

## Installation

```bash
$ pip install huawei-lte-api
```

## Usage

```python3
from huawei_lte_api.Client import Client
from huawei_lte_api.AuthorizedConnection import AuthorizedConnection
from huawei_lte_api.Connection import Connection

# connection = Connection('http://192.168.8.1/') For limited access, I have valid credentials no need for limited access
# connection = AuthorizedConnection('http://admin:MY_SUPER_TRUPER_PASSWORD@192.168.8.1/', login_on_demand=True) # If you wish to login on demand (when call requires authorization), pass login_on_demand=True
connection = AuthorizedConnection('http://admin:MY_SUPER_TRUPER_PASSWORD@192.168.8.1/')

client = Client(connection) # This just simplifies access to separate API groups, you can use device = Device(connection) if you want

print(client.device.signal())  # Can be accessed without authorization
print(client.device.information())  # Needs valid authorization, will throw exception if invalid credentials are passed in URL


# For more API calls just look on code in the huawei_lte_api/api folder, there is no separate DOC yet

```
Result dict
```python
{'DeviceName': 'B310s-22', 'SerialNumber': 'MY_SERIAL_NUMBER', 'Imei': 'MY_IMEI', 'Imsi': 'MY_IMSI', 'Iccid': 'MY_ICCID', 'Msisdn': None, 'HardwareVersion': 'WL1B310FM03', 'SoftwareVersion': '21.311.06.03.55', 'WebUIVersion': '17.100.09.00.03', 'MacAddress1': 'EHM:MY:MAC', 'MacAddress2': None, 'ProductFamily': 'LTE', 'Classify': 'cpe', 'supportmode': None, 'workmode': 'LTE'}
```
