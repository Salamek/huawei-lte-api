from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class Cradle(ApiGroup):
    def status_info(self) ->dict:
        return self._connection.get('cradle/status-info')

    def feature_switch(self) ->dict:
        return self._connection.get('cradle/feature-switch')

    @authorized_call
    def basic_info(self) -> dict:
        return self._connection.get('cradle/basic-info')

    @authorized_call
    def factory_mac(self) -> dict:
        return self._connection.get('cradle/factory-mac')

    @authorized_call
    def mac_info(self) -> dict:
        return self._connection.get('cradle/mac-info')
