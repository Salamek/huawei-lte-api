
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class Redirection(ApiGroup):
    def homepage(self) -> dict:
        return self._connection.get('redirection/homepage')