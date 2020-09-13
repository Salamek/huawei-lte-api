from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class Voice(ApiGroup):
    def config(self) -> GetResponseType:
        return self._connection.get('voice/config.xml', prefix='config')

    def country(self) -> GetResponseType:
        return self._connection.get('voice/country.xml', prefix='config')
