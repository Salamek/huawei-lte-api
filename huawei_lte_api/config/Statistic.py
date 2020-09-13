from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class Statistic(ApiGroup):
    def config(self) -> GetResponseType:
        return self._connection.get('statistic/config.xml', prefix='config')
