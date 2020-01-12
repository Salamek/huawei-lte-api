from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class Cradle(ApiGroup):
    def status_info(self) -> GetResponseType:
        return self._connection.get('cradle/status-info')

    def feature_switch(self) -> GetResponseType:
        return self._connection.get('cradle/feature-switch')

    def basic_info(self) -> GetResponseType:
        return self._connection.get('cradle/basic-info')

    def factory_mac(self) -> GetResponseType:
        return self._connection.get('cradle/factory-mac')

    def mac_info(self) -> GetResponseType:
        return self._connection.get('cradle/mac-info')
