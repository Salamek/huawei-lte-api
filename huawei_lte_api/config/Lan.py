from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Lan(ApiGroup):
    def config(self) -> GetResponseType:
        return self._session.get('lan/config.xml', prefix='config')
