from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class FastBoot(ApiGroup):
    def config(self) -> GetResponseType:
        return self._connection.get('fastboot/config.xml', prefix='config')
