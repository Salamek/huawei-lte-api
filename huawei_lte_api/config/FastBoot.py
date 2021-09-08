from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class FastBoot(ApiGroup):
    def config(self) -> GetResponseType:
        return self._session.get('fastboot/config.xml', prefix='config')
