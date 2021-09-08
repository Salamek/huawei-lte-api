from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Statistic(ApiGroup):
    def config(self) -> GetResponseType:
        return self._session.get('statistic/config.xml', prefix='config')
