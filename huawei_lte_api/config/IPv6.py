from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class IPv6(ApiGroup):
    def config(self) -> GetResponseType:
        return self._session.get('ipv6/config.xml', prefix='config')
