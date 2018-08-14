
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class Pin(ApiGroup):
    def status(self) -> dict:
        return self._connection.get('pin/status')

    def simlock(self) -> dict:
        return self._connection.get('pin/simlock')