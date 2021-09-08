from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Update(ApiGroup):
    def config(self) -> GetResponseType:
        return self._session.get('update/config.xml', prefix='config')
