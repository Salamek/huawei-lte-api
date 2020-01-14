from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class Stk(ApiGroup):
    def config(self) -> GetResponseType:
        return self._connection.get('stk/config.xml', prefix='config')
