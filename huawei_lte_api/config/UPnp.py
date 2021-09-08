from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class UPnp(ApiGroup):
    def config(self) -> GetResponseType:
        return self._session.get('upnp/config.xml', prefix='config')
