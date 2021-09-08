from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Voice(ApiGroup):
    def config(self) -> GetResponseType:
        return self._session.get('voice/config.xml', prefix='config')

    def country(self) -> GetResponseType:
        return self._session.get('voice/country.xml', prefix='config')
