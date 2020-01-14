from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class Pb(ApiGroup):
    def config(self) -> GetResponseType:
        return self._connection.get('pb/config.xml', prefix='config')
