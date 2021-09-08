from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Pb(ApiGroup):
    def config(self) -> GetResponseType:
        return self._session.get('pb/config.xml', prefix='config')
