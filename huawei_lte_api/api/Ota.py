from huawei_lte_api.ApiGroup import ApiGroup, GetResponseType


class Ota(ApiGroup):
    def status(self) -> GetResponseType:
        return self._connection.get('ota/status')
