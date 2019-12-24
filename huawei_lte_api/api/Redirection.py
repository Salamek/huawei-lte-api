from huawei_lte_api.ApiGroup import ApiGroup, GetResponseType


class Redirection(ApiGroup):
    def homepage(self) -> GetResponseType:
        return self._connection.get('redirection/homepage')
