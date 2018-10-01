
from huawei_lte_api.ApiGroup import ApiGroup


class Ota(ApiGroup):
    def status(self) -> dict:
        return self._connection.get('ota/status')
