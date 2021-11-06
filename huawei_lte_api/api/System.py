from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class System(ApiGroup):
    def devcapacity(self) -> GetResponseType:
        return self._session.get('system/devcapacity')
