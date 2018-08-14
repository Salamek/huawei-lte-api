
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class Ota(ApiGroup):
    def status(self) -> dict:
        return self._connection.get('ota/status')