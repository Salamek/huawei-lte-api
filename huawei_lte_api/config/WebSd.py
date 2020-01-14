from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class WebSd(ApiGroup):
    def config(self) -> GetResponseType:
        return self._connection.get('websd/config.xml', prefix='config')
