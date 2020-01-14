from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class Sntp(ApiGroup):
    def config(self) -> GetResponseType:
        return self._connection.get('sntp/config.xml', prefix='config')
