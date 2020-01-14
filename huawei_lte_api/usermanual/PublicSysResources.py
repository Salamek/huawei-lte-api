from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class PublicSysResources(ApiGroup):
    def config(self) -> GetResponseType:
        return self._connection.get('public_sys-resources/config.xml', prefix='usermanual')
