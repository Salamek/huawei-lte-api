
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class WLan(ApiGroup):
    def wifi_feature_switch(self):
        return self.connection.get('wlan/wifi-feature-switch')

    def station_information(self):
        return self.connection.get('wlan/station-information')

    def basic_settings(self):
        return self.connection.get('wlan/basic-settings')

    @authorized_call
    def multi_security_settings(self):
        return self.connection.get('wlan/multi-security-settings')