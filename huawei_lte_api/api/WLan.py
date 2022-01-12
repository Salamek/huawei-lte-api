from collections import OrderedDict

from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType, SetResponseType
from huawei_lte_api.enums.wlan import AuthModeEnum, WepEncryptModeEnum, WpaEncryptModeEnum
from huawei_lte_api.Tools import Tools


def _to_multi_basic_settings_ssid_body(ssid: dict) -> dict:
    wanted_items = (
        'Index',
        'WifiBroadcast',
        'wifiguestofftime',
        'WifiAuthmode',
        'ID',
        'WifiEnable',
        'wifiisguestnetwork',
        'WifiMac',
        'WifiSsid',
        'WifiRadiusKey',
        'WifiWpaencryptionmodes',
        'WifiWepKeyIndex'
    )
    return Tools.filter_dict(ssid, wanted_items)


def _set_wifi_enable(ssid: dict, status: bool) -> dict:
    if ssid.get('wifiisguestnetwork') == '0':
        return ssid

    ssid['WifiEnable'] = '1' if status else '0'
    return ssid


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
        Turn on/off wifi guest network
        :param status: True->on, False->off
        """
        multi_basic_settings = self.multi_basic_settings()
        ssids = map(_to_multi_basic_settings_ssid_body, multi_basic_settings['Ssids']['Ssid'])
        ssids = map(lambda ssid: _set_wifi_enable(ssid, status), ssids)
        return self.set_multi_basic_settings(list(ssids))

    def wlandbho(self) -> GetResponseType:
        return self._session.get('wlan/wlandbho')

    def wlanintelligent(self) -> GetResponseType:
        return self._session.get('wlan/wlanintelligent')
