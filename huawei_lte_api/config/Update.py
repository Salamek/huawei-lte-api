from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class Update(ApiGroup):
    def config(self) -> GetResponseType:
        return self._connection.get('update/config.xml', prefix='config')
