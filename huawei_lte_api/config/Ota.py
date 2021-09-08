from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Ota(ApiGroup):
    def config(self) -> GetResponseType:
        return self._session.get('ota/config.xml', prefix='config')
