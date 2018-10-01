
from huawei_lte_api.ApiGroup import ApiGroup


class Pin(ApiGroup):
    def status(self) -> dict:
        return self._connection.get('pin/status')

    def simlock(self) -> dict:
        return self._connection.get('pin/simlock')
