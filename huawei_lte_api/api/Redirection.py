from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class Redirection(ApiGroup):
    def homepage(self) -> GetResponseType:
        return self._connection.get('redirection/homepage')
