from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Redirection(ApiGroup):
    def homepage(self) -> GetResponseType:
        return self._session.get('redirection/homepage')
