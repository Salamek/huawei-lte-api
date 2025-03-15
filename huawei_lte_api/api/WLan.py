import dataclasses
from collections import OrderedDict
from typing import List, Optional, Iterable, Dict, Any, Union

from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType, SetResponseType
from huawei_lte_api.enums.wlan import AuthModeEnum, WepEncryptModeEnum, WpaEncryptModeEnum
from huawei_lte_api.Tools import Tools

# Constants for repeated string patterns
WIFI_MAC_FILTER_MAC_TEMPLATE = 'WifiMacFilterMac{}'
WIFI_HOSTNAME_TEMPLATE = 'wifihostname{}'


@dataclasses.dataclass
class WLanSettings:
    index: int
    enabled: bool
    ssid: str
    mac: Optional[str]
    broadcast: bool
    auth_mode: str
    id: Optional[str]
    radius_key: Optional[str]
    wpa_encryption_modes: str
    wep_key_index: int
    guest_off_time: int
    is_guest_network: bool

    @classmethod
    def from_dict(cls, data: dict) -> 'WLanSettings':
        return WLanSettings(
            index=int(data.get('Index', 0)),
            enabled=data.get('WifiEnable') == '1',
            ssid=data.get('WifiSsid', ''),
            mac=data.get('WifiMac'),
            broadcast=data.get('WifiBroadcast') == '1',
            auth_mode=data.get('WifiAuthmode', ''),
            wpa_encryption_modes=data.get('WifiWpaencryptionmodes', ''),
            wep_key_index=int(data.get('WifiWepKeyIndex', 0)),
            guest_off_time=int(data.get('wifiguestofftime', 0)),
            is_guest_network=data.get('wifiisguestnetwork', '0') == '1',
            id=data.get('ID'),
            radius_key=data.get('WifiRadiusKey')
        )

    def to_dict(self) -> dict:
        return {
            'Index': str(self.index),
            'WifiEnable': '1' if self.enabled else '0',
            'WifiSsid': self.ssid,
            'WifiMac': self.mac,
            'WifiBroadcast': '1' if self.broadcast else '0',
            'WifiAuthmode': self.auth_mode,
            'WifiWpaencryptionmodes': self.wpa_encryption_modes,
            'WifiWepKeyIndex': str(self.wep_key_index),
            'wifiguestofftime': str(self.guest_off_time)
        }


class WLan(ApiGroup):
    def wifi_feature_switch(self) -> GetResponseType:
        return self._session.get('wlan/wifi-feature-switch')

    def station_information(self) -> GetResponseType:
        return self._session.get('wlan/station-information')

    def basic_settings(self) -> GetResponseType:
        return self._session.get('wlan/basic-settings')

    def set_basic_settings(self, ssid: str, hide: bool = False, wifi_restart: bool = False) -> SetResponseType:
        return self._session.post_set('wlan/basic-settings', OrderedDict((
            ('WifiSsid', ssid),
            ('WifiHide', hide),
            ('WifiRestart', int(wifi_restart))
        )))

    def security_settings(self) -> GetResponseType:
        return self._session.get('wlan/security-settings')

    def set_security_settings(self,
                              wpa_psk: str,
                              wep_key: str = '',
                              wpa_encryption_mode: WpaEncryptModeEnum = WpaEncryptModeEnum.MIX,
                              wep_encryption_mode: WepEncryptModeEnum = WepEncryptModeEnum.WEP128,
                              auth_mode: AuthModeEnum = AuthModeEnum.AUTO,
                              wifi_restart: bool = True
                              ) -> SetResponseType:
        return self._session.post_set('wlan/security-settings', OrderedDict((
            ('WifiAuthmode', auth_mode.value),
            ('WifiWepKey1', wep_key),
            ('WifiWpaencryptionmodes', wpa_encryption_mode.value),
            ('WifiBasicencryptionmodes', wep_encryption_mode.value),
            ('WifiWpapsk', wpa_psk),
            ('WifiRestart', int(wifi_restart))
        )))

    def multi_security_settings(self) -> GetResponseType:
        return self._session.get('wlan/multi-security-settings')

    def multi_security_settings_ex(self) -> GetResponseType:
        return self._session.get('wlan/multi-security-settings-ex')

    def multi_basic_settings(self) -> GetResponseType:
        return self._session.get('wlan/multi-basic-settings')

    def set_multi_basic_settings(self, clients: list) -> SetResponseType:
        """

        :param clients: list of dicts with format {'wifihostname': hostname,'WifiMacFilterMac': mac}
        """
        return self._session.post_set('wlan/multi-basic-settings', {
            'Ssids': {
                'Ssid': clients
            },
            'WifiRestart': 1
        })

    def host_list(self) -> GetResponseType:
        hosts = self._session.get('wlan/host-list')
        # Make sure Hosts->Host is a list
        # It may be returned as a single dict if only one is associated,
        # as well as sometimes None.
        return Tools.enforce_list_response(hosts, 'Host')

    def handover_setting(self) -> GetResponseType:
        return self._session.get('wlan/handover-setting')

    def set_handover_setting(self, handover: int) -> SetResponseType:
        """
        G3_PREFER = 0
        WIFI_PREFER = 2
        :param handover:
        """
        return self._session.post_set('wlan/handover-setting', {
            'Handover': handover
        })

    def multi_switch_settings(self) -> GetResponseType:
        return self._session.get('wlan/multi-switch-settings')

    def multi_macfilter_settings(self) -> GetResponseType:
        return self._session.get('wlan/multi-macfilter-settings')

    def set_multi_macfilter_settings(self, clients: list) -> SetResponseType:
        """
        :param clients: list of dicts with format {'WifiMacFilterMac0': 'mac address','wifihostname0': 'name', 'Index': 'number', 'WifiMacFilterStatus': 'number(1 or 2)'}
        """
        return self._session.post_set('wlan/multi-macfilter-settings', {
            'Ssids': {
                'Ssid': clients
            }
        })

    def multi_macfilter_settings_ex(self) -> GetResponseType:
        return self._session.get('wlan/multi-macfilter-settings-ex')

    def mac_filter(self) -> GetResponseType:
        return self._session.get('wlan/mac-filter')

    def set_mac_filter(self, hostname: str, mac: str) -> SetResponseType:
        return self._session.post_set('wlan/mac-filter', OrderedDict((
            ('wifihostname', hostname),
            ('WifiMacFilterMac', mac)
        )))

    def oled_showpassword(self) -> GetResponseType:
        return self._session.get('wlan/oled-showpassword')

    def wps(self) -> GetResponseType:
        return self._session.get('wlan/wps')

    def wps_appin(self) -> GetResponseType:
        return self._session.get('wlan/wps-appin')

    def set_wps_appin(self, wpsappintype: int = 0, wpsappin: Optional[int] = None) -> SetResponseType:
        return self._session.post_set('wlan/wps-appin', OrderedDict((
            ('wpsappintype', wpsappintype),
            ('wpsappin', str(wpsappin) if wpsappin is not None else ''),
        )))

    def wps_pbc(self) -> GetResponseType:
        return self._session.get('wlan/wps-pbc')

    def set_wps_pbc(self, wpsmode: int = 1, ssidindex: int = 0) -> SetResponseType:
        return self._session.post_set('wlan/wps-pbc', OrderedDict((
            ('WPSMode', wpsmode),
            ('ssidindex', ssidindex),
        )))

    def wps_switch(self) -> GetResponseType:
        return self._session.get('wlan/wps-switch')

    def set_wps_switch(self, appinenable: int) -> SetResponseType:
        return self._session.post_set('wlan/wps-switch', OrderedDict((
            ('appinenable', appinenable),
        )))

    def status_switch_settings(self) -> GetResponseType:
        return self._session.get('wlan/status-switch-settings')

    def wifiprofile(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage, probably not implemented by Huawei
        :return:
        """
        return self._session.get('wlan/wifiprofile')

    def wififrequence(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage, probably not implemented by Huawei
        :return:
        """
        return self._session.get('wlan/wififrequence')

    def wifiscanresult(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage, probably not implemented by Huawei
        :return:
        """
        return self._session.get('wlan/wifiscanresult')

    def wifi_guest_network_switch(self, status: bool) -> SetResponseType:
        """
        Turn on/off Wi-Fi guest network
        :param status: True->on, False->off
        """

        return self.wifi_network_switch(status, {'is_guest_network': True})

    def find_wlan_settings(self, criteria: dict) -> List[WLanSettings]:
        """
        Finds WLanSettings by provided criteria
        :param criteria: dict of key: value
        :return: List[WLanSettings]
        """
        multi_basic_settings = self.multi_basic_settings()
        ssids = map(WLanSettings.from_dict, multi_basic_settings['Ssids']['Ssid'])
        return list(Tools.filter_iter(ssids, criteria))

    def save_wlan_settings(self, settings: Iterable[WLanSettings]) -> SetResponseType:
        """
        Saves modified list of WLanSettings
        :param settings:
        :return: SetResponseType
        """
        return self.set_multi_basic_settings([item.to_dict() for item in settings])

    def wifi_network_switch(self, status: bool, criteria: Optional[dict] = None) -> SetResponseType:
        """
        Turn on/off Wi-Fi network by criteria, by default matches all wlans
        :param status: True->on, False->off
        :param criteria: Optional criteria to filter networks
        """
        items = self.find_wlan_settings(criteria or {})
        for item in items:
            item.enabled = status

        return self.save_wlan_settings(items)

    def wlandbho(self) -> GetResponseType:
        return self._session.get('wlan/wlandbho')

    def wlan_guide_settings(self) -> GetResponseType:
        return self._session.get('wlan/wlan-guide-settings')

    def set_wlan_guide_settings(self, ssid: str, wpa_psk: str, current_password: str, new_password: str) -> SetResponseType:
        ssids = self.wlan_guide_settings()["Ssids"]["Ssid"]
        new_ssid = ssids[0] if len(ssids) > 0 else {"Index": "0"}
        new_ssid["WifiSsid"] = ssid
        new_ssid["WifiWpapsk"] = wpa_psk

        self._session.reload()

        data = {
            "Ssids": {
                "Ssid": [new_ssid]
            },
            "rebootInfo": {
                "isReboot": 0
            },
            "accountInfo": {
                "currentpassword": current_password,
                "newpassword": new_password,
                "confirmpwd": new_password}
        }
        return self._session.post_set('wlan/wlan-guide-settings',
                                      data,
                                      refresh_csrf=True,
                                      is_encrypted=True)

    def wlanintelligent(self) -> GetResponseType:
        return self._session.get('wlan/wlanintelligent')

    def filter_mac_addresses(self, mac_list: List[str], hostname_list: List[str],
                             ssid_index: str = '0', filter_status: str = '2') -> SetResponseType:
        """
        Add multiple MAC addresses to the filter list

        :param mac_list: List of MAC addresses to filter
        :param hostname_list: List of hostnames corresponding to the MAC addresses
        :param ssid_index: SSID index (default: '0')
        :param filter_status: '1' for whitelist, '2' for blacklist (default: '2')
        :return: API response

        Example:
            wlan.filter_mac_addresses(
                ['11:22:33:44:55:66', 'AA:BB:CC:DD:EE:FF'],
                ['Device1', 'Device2'],
                ssid_index='0',
                filter_status='2'
            )
        """
        if len(mac_list) != len(hostname_list):
            raise ValueError("The number of MAC addresses and hostnames must be the same")

        clients = {
            'Index': ssid_index,
            'WifiMacFilterStatus': filter_status
        }

        # Add each MAC address with the correct index
        for i, (mac, hostname) in enumerate(zip(mac_list, hostname_list)):
            clients[WIFI_MAC_FILTER_MAC_TEMPLATE.format(i)] = mac
            clients[WIFI_HOSTNAME_TEMPLATE.format(i)] = hostname

        return self.set_multi_macfilter_settings([clients])

    def _extract_mac_hostname_pairs(self, mac_list_dict: Optional[Dict[str, str]]) -> List[Dict[str, str]]:
        """Helper method to extract MAC address and hostname pairs from response dictionary"""
        devices: List[Dict[str, str]] = []
        if not isinstance(mac_list_dict, dict):
            return devices

        i = 0
        while WIFI_MAC_FILTER_MAC_TEMPLATE.format(i) in mac_list_dict:
            mac_key = WIFI_MAC_FILTER_MAC_TEMPLATE.format(i)
            hostname_key = WIFI_HOSTNAME_TEMPLATE.format(i)

            mac = mac_list_dict.get(mac_key, '')
            hostname = mac_list_dict.get(hostname_key, '')

            if mac:
                devices.append({'mac': mac, 'hostname': hostname})
            i += 1

        return devices

    def get_filtered_devices(self) -> List[Dict[str, Any]]:
        """
        Get a structured list of MAC addresses in the filter lists (both blacklist and whitelist)

        :return: List of dictionaries containing filtered device information
        """
        response = self.multi_macfilter_settings_ex()
        result: List[Dict[str, Any]] = []

        if 'Ssids' not in response or 'Ssid' not in response['Ssids']:
            return result

        for ssid in response['Ssids']['Ssid']:
            ssid_index = ssid.get('Index', '')

            # Process blacklist
            blacklist = ssid.get('wifimacblacklist')
            blacklist_devices = self._extract_mac_hostname_pairs(blacklist) if blacklist else []
            result.append({
                'ssid_index': ssid_index,
                'filter_type': 'blacklist',
                'devices': blacklist_devices
            })

            # Process whitelist
            whitelist = ssid.get('wifimacwhitelist')
            whitelist_devices = self._extract_mac_hostname_pairs(whitelist) if whitelist else []
            result.append({
                'ssid_index': ssid_index,
                'filter_type': 'whitelist',
                'devices': whitelist_devices
            })

        return result

    def get_filter_status(self) -> Dict[str, Union[bool, str]]:
        """
        Get the current MAC filter status (enabled/disabled and mode)

        :return: Dictionary with filter status information

        Example response:
        {
            'enabled': True,  # Whether MAC filtering is enabled
            'mode': 'blacklist'  # 'blacklist' or 'whitelist'
        }
        """
        response = self.multi_macfilter_settings_ex()

        enabled = response.get('enable', '0') == '1'
        # Filter status: '1' for whitelist, '2' for blacklist
        filter_status = response.get('wifimacfilterstatus', '2')
        mode = 'whitelist' if filter_status == '1' else 'blacklist'

        return {
            'enabled': enabled,
            'mode': mode
        }
