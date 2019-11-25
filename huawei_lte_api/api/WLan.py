from collections import OrderedDict
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.enums.wlan import AuthModeEnum, WepEncryptModeEnum, WpaEncryptModeEnum


class WLan(ApiGroup):
    def wifi_feature_switch(self) -> dict:
        return self._connection.get('wlan/wifi-feature-switch')

    def station_information(self) -> dict:
        return self._connection.get('wlan/station-information')

    def basic_settings(self) -> dict:
        return self._connection.get('wlan/basic-settings')

    def set_basic_settings(self, ssid: str, hide: bool=False, wifi_restart: bool=False):
        return self._connection.post('wlan/basic-settings', OrderedDict((
            ('WifiSsid', ssid),
            ('WifiHide', hide),
            ('WifiRestart', int(wifi_restart))
        )))

    def security_settings(self) -> dict:
        return self._connection.get('wlan/security-settings')

    def set_security_settings(self,
                              wpa_psk: str,
                              wep_key: str='',
                              wpa_encryption_mode: WpaEncryptModeEnum=WpaEncryptModeEnum.MIX,
                              wep_encryption_mode: WepEncryptModeEnum=WepEncryptModeEnum.WEP128,
                              auth_mode: AuthModeEnum=AuthModeEnum.AUTO,
                              wifi_restart: bool=True
                              ):
        return self._connection.post('wlan/security-settings', OrderedDict((
            ('WifiAuthmode', auth_mode.value),
            ('WifiWepKey1', wep_key),
            ('WifiWpaencryptionmodes', wpa_encryption_mode.value),
            ('WifiBasicencryptionmodes', wep_encryption_mode.value),
            ('WifiWpapsk', wpa_psk),
            ('WifiRestart', int(wifi_restart))
        )))

    def multi_security_settings(self) -> dict:
        return self._connection.get('wlan/multi-security-settings')

    def multi_security_settings_ex(self) -> dict:
        return self._connection.get('wlan/multi-security-settings-ex')

    def multi_basic_settings(self) -> dict:
        return self._connection.get('wlan/multi-basic-settings')

    def set_multi_basic_settings(self, clients: list) -> dict:
        """

   :param clients: list of dicts with format {'wifihostname': hostname,'WifiMacFilterMac': mac}
   :return: dict
   """
        return self._connection.post('wlan/multi-basic-settings', {
            'Ssids': {
                'Ssid': clients
            },
            'WifiRestart': 1
        })

    def host_list(self) -> dict:
        # Make sure Hosts->Host is a list
        # It may be returned as a single dict if only one is associated,
        # as well as sometimes None.
        hosts = self._connection.get('wlan/host-list')
        if hosts.get('Hosts') is None:
            hosts['Hosts'] = {}
        host = hosts['Hosts'].setdefault('Host', [])
        if isinstance(host, dict):
            hosts['Hosts']['Host'] = [host]
        return hosts

    def handover_setting(self) -> dict:
        return self._connection.get('wlan/handover-setting')

    def set_handover_setting(self, handover: int):
        """
    G3_PREFER = 0
    WIFI_PREFER = 2
    :param handover:
    :return:
    """
        return self._connection.post('wlan/handover-setting', {
            'Handover': handover
        })

    def multi_switch_settings(self) -> dict:
        return self._connection.get('wlan/multi-switch-settings')

    def multi_macfilter_settings(self) -> dict:
        return self._connection.get('wlan/multi-macfilter-settings')

    def set_multi_macfilter_settings(self, clients: list) -> dict:
        """

        :param clients: list of dicts with format {'wifihostname': hostname,'WifiMacFilterMac': mac}
        :return: dict
        """
        return self._connection.post('wlan/multi-macfilter-settings', {
            'Ssids': {
                'Ssid': clients
            }
        })

    def multi_macfilter_settings_ex(self) -> dict:
        return self._connection.get('wlan/multi-macfilter-settings-ex')

    def mac_filter(self) -> dict:
        return self._connection.get('wlan/mac-filter')

    def set_mac_filter(self, hostname: str, mac: str):
        return self._connection.post('wlan/mac-filter', OrderedDict((
            ('wifihostname', hostname),
            ('WifiMacFilterMac', mac)
        )))

    def oled_showpassword(self) -> dict:
        return self._connection.get('wlan/oled-showpassword')

    def wps(self) -> dict:
        return self._connection.get('wlan/wps')

    def wps_appin(self) -> dict:
        return self._connection.get('wlan/wps-appin')

    def wps_pbc(self) -> dict:
        return self._connection.get('wlan/wps-pbc')

    def wps_switch(self) -> dict:
        return self._connection.get('wlan/wps-switch')

    def status_switch_settings(self) -> dict:
        return self._connection.get('wlan/status-switch-settings')
