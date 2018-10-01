
from huawei_lte_api.ApiGroup import ApiGroup


class Dhcp(ApiGroup):
    def settings(self) -> dict:
        return self._connection.get('dhcp/settings')

    def feature_switch(self) -> dict:
        return self._connection.get('dhcp/feature-switch')
