from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Time(ApiGroup):

    def timeout(self) -> GetResponseType:
        return self._session.get('time/timeout')
