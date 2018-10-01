
from huawei_lte_api.ApiGroup import ApiGroup


class Redirection(ApiGroup):
    def homepage(self) -> dict:
        return self._connection.get('redirection/homepage')
