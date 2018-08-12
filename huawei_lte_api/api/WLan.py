
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class WLan(ApiGroup):
    def wifi_feature_switch(self):
        return self._connection.get('wlan/wifi-feature-switch')

    def station_information(self):
        return self._connection.get('wlan/station-information')

    def basic_settings(self):
        return self._connection.get('wlan/basic-settings')

    @authorized_call
    def multi_security_settings(self):
        return self._connection.get('wlan/multi-security-settings')

    def handover_setting(self):
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

    def multi_switch_settings(self):
        return self._connection.get('wlan/multi-switch-settings')