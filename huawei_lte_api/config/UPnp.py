from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class UPnp(ApiGroup):
    def config(self) -> GetResponseType:
        return self._connection.get('upnp/config.xml', prefix='config')
