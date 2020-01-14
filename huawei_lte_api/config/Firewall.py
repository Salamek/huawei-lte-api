from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class Firewall(ApiGroup):
    def config(self) -> GetResponseType:
        return self._connection.get('firewall/config.xml', prefix='config')
