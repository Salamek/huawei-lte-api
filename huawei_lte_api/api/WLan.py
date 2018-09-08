
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call
from huawei_lte_api.enums.wlan import AuthModeEnum, WepEncryptModeEnum, WpaEncryptModeEnum


class WLan(ApiGroup):
    def wifi_feature_switch(self) -> dict:
        return self._connection.get('wlan/wifi-feature-switch')

    def station_information(self) -> dict:
        return self._connection.get('wlan/station-information')

    def basic_settings(self) -> dict:
        return self._connection.get('wlan/basic-settings')

    @authorized_call
    def set_basic_settings(self, ssid: str, hide: bool=False, wifi_restart: bool=False):
        return self._connection.post('wlan/basic-settings', {
            'WifiSsid': ssid,
            'WifiHide': hide,
            'WifiRestart': int(wifi_restart)
        })

    @authorized_call
    def security_settings(self) -> dict:
        return self._connection.get('wlan/security-settings')

    @authorized_call
    def set_security_settings(self,
                              wpa_psk: str,
                              wep_key: str='',
                              wpa_encryption_mode: WpaEncryptModeEnum=WpaEncryptModeEnum.MIX,
                              wep_encryption_mode: WepEncryptModeEnum=WepEncryptModeEnum.WEP128,
                              auth_mode: AuthModeEnum=AuthModeEnum.AUTO,
                              wifi_restart: bool=True
                              ):
        return self._connection.post('wlan/security-settings', {
            'WifiAuthmode': auth_mode.value,
            'WifiWepKey1': wep_key,
            'WifiWpaencryptionmodes': wpa_encryption_mode.value,
            'WifiBasicencryptionmodes': wep_encryption_mode.value,
            'WifiWpapsk': wpa_psk,
            'WifiRestart': int(wifi_restart)
        })

    @authorized_call
    def multi_security_settings(self) -> dict:
        return self._connection.get('wlan/multi-security-settings')

    @authorized_call
    def multi_security_settings_ex(self) -> dict:
        return self._connection.get('wlan/multi-security-settings-ex')

    @authorized_call
    def multi_basic_settings(self) -> dict:
        return self._connection.get('wlan/multi-basic-settings')

    @authorized_call
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

    @authorized_call
    def host_list(self) -> dict:
        return self._connection.get('wlan/host-list')

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

    @authorized_call
    def multi_macfilter_settings(self) -> dict:
        return self._connection.get('wlan/multi-macfilter-settings')

    @authorized_call
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

    @authorized_call
    def mac_filter(self) -> dict:
        return self._connection.get('wlan/mac-filter')

    @authorized_call
    def set_mac_filter(self, hostname: str, mac: str):
        return self._connection.post('wlan/mac-filter', {
            'wifihostname': hostname,
            'WifiMacFilterMac': mac
        })

    @authorized_call
    def oled_showpassword(self) -> dict:
        return self._connection.get('wlan/oled-showpassword')

    @authorized_call
    def wps(self) -> dict:
        return self._connection.get('wlan/wps')

    @authorized_call
    def wps_appin(self) -> dict:
        return self._connection.get('wlan/wps-appin')

    @authorized_call
    def wps_pbc(self) -> dict:
        return self._connection.get('wlan/wps-pbc')

    @authorized_call
    def wps_switch(self) -> dict:
        return self._connection.get('wlan/wps-switch')
