from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class WebSd(ApiGroup):
    def config(self) -> GetResponseType:
        return self._session.get('websd/config.xml', prefix='config')
