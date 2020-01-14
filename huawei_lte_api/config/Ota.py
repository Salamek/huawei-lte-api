from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class Ota(ApiGroup):
    def config(self) -> GetResponseType:
        return self._connection.get('ota/config.xml', prefix='config')
