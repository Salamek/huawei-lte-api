from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Ota(ApiGroup):
    def status(self) -> GetResponseType:
        return self._session.get('ota/status')
