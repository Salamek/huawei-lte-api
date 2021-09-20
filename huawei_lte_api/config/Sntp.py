from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Sntp(ApiGroup):
    def config(self) -> GetResponseType:
        return self._session.get('sntp/config.xml', prefix='config')
