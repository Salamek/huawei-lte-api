# huawei-lte-api
API For huawei LAN/WAN LTE Modems,
you can use this to simply send SMS, get information about your internet usage, signal, and tons of other stuff

[![Tox tests](https://github.com/Salamek/huawei-lte-api/actions/workflows/python-test.yml/badge.svg)](https://github.com/Salamek/huawei-lte-api/actions/workflows/python-test.yml)

> Please consider sponsoring if you're using this package commercially, my time is not free :) You can sponsor me by clicking on "Sponsor" button in top button row. Thank You.


## Tested on:
#### 3G/LTE Routers:
* Huawei B310s-22
* Huawei B311-221
* Huawei B315s-22
* Huawei B525s-23a
* Huawei B525s-65a
* Huawei B715s-23c
* Huawei B528s
* Huawei B535-232
* Huawei B628-265
* Huawei B612-233
* Huawei B818-263
* Huawei E5180s-22
* Huawei E5186s-22a
* Huawei E5576-320
* Huawei E5577Cs-321
* Huawei E8231
* Huawei E5573s-320
* SoyeaLink B535-333
  
 
#### 3G/LTE USB sticks:
(Device must support NETWork mode aka. "HiLink" version, it wont work with serial mode)
* Huawei E3131
* Huawei E8372h-608
* Huawei E3372
* Huawei E3531
* Huawei E5530As-2


#### 5G Routers:
* Huawei 5G CPE Pro 2 (H122-373)
* Huawei 5G CPE Pro (H112-372)

(probably will work for other Huawei LTE devices too)

### Will NOT work on:
#### LTE Routers:
* Huawei B2368-22 (Incompatible firmware, testing device needed!)
* Huawei B593s-22 (Incompatible firmware, testing device needed!)


## Installation

### PIP (pip3 on some distros)
```bash
pip install huawei-lte-api
```
### Repository
You can also use these repositories maintained by me
#### Debian and derivatives

Add repository by running these commands

```bash
wget -O- https://repository.salamek.cz/deb/salamek.gpg | sudo tee /usr/share/keyrings/salamek-archive-keyring.gpg
echo "deb     [signed-by=/usr/share/keyrings/salamek-archive-keyring.gpg] https://repository.salamek.cz/deb/pub all main" | sudo tee /etc/apt/sources.list.d/salamek.cz.list
```

And then you can install a package python3-huawei-lte-api

```bash
apt update && apt install python3-huawei-lte-api
```

#### Archlinux

Add repository by adding this at end of file /etc/pacman.conf

```
[salamek]
Server = https://repository.salamek.cz/arch/pub/any
SigLevel = Optional
```

and then install by running

```bash
pacman -Sy python-huawei-lte-api
```

#### Gentoo

```bash
emerge dev-python/huawei-lte-api
```


## Usage

```python3
from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection

# with Connection('http://192.168.8.1/') as connection: For limited access, I have valid credentials no need for limited access
with Connection('http://admin:MY_SUPER_TRUPER_PASSWORD@192.168.8.1/') as connection:
    client = Client(connection) # This just simplifies access to separate API groups, you can use device = Device(connection) if you want

    print(client.device.signal())  # Can be accessed without authorization
    print(client.device.information())  # Needs valid authorization, will throw exception if invalid credentials are passed in URL


# For more API calls just look on code in the huawei_lte_api/api folder, there is no separate DOC yet

```
Result dict
```python
{'DeviceName': 'B310s-22', 'SerialNumber': 'MY_SERIAL_NUMBER', 'Imei': 'MY_IMEI', 'Imsi': 'MY_IMSI', 'Iccid': 'MY_ICCID', 'Msisdn': None, 'HardwareVersion': 'WL1B310FM03', 'SoftwareVersion': '21.311.06.03.55', 'WebUIVersion': '17.100.09.00.03', 'MacAddress1': 'EHM:MY:MAC', 'MacAddress2': None, 'ProductFamily': 'LTE', 'Classify': 'cpe', 'supportmode': None, 'workmode': 'LTE'}
```

## Code examples

Some code [examples](examples/) are in [/examples](examples/)  folder

### Monitoring

* Monitoring traffic and signal https://github.com/littlejo/huawei-lte-examples
* Set band, show signal level and bandwidth for Huawei mobile broadband B525s-23a. https://github.com/octave21/huawei-lte
* Application that monitors Internet connectivity and restarts router when internet is not reachable https://github.com/Salamek/netkeeper
* Monitoring app with nice TUI interface (just like htop) https://github.com/pdo-smith/5gtop

### SMS

* Relay received SMS into your email https://github.com/chenwei791129/Huawei-LTE-Router-SMS-to-E-mail-Sender

## Ports to other languages

* TypeScript/JavaScript https://github.com/Salamek/huawei-lte-api-ts
* PHP https://github.com/icetee/huawei-lte-api-php

## Donations

* 250 CZK (9.79 EUR) for B535-232 fund, thx @larsvinc !
* 371,69 CZK (14.32 EUR) by Oleg Jusaew
* 292 CZK (11.50 EUR) by Toth-Mate Akos
