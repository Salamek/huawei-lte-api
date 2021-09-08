from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Stk(ApiGroup):
    def config(self) -> GetResponseType:
        return self._session.get('stk/config.xml', prefix='config')
