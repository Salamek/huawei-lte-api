from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Staticroute(ApiGroup):
    def wanpath(self) -> GetResponseType:
        return self._session.get('staticroute/wanpath')
