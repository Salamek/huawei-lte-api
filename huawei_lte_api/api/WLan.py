import dataclasses
from collections import OrderedDict
from typing import List, Optional, Iterable

from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType, SetResponseType
from huawei_lte_api.enums.wlan import AuthModeEnum, WepEncryptModeEnum, WpaEncryptModeEnum
from huawei_lte_api.Tools import Tools


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

        :param clients: list of dicts with format {'wifihostname': hostname,'WifiMacFilterMac': mac}
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

    def wps_pbc(self) -> GetResponseType:
        return self._session.get('wlan/wps-pbc')

    def wps_switch(self) -> GetResponseType:
        return self._session.get('wlan/wps-switch')

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

    def wlanintelligent(self) -> GetResponseType:
        return self._session.get('wlan/wlanintelligent')
