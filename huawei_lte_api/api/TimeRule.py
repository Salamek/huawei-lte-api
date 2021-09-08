from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class TimeRule(ApiGroup):

    def timerule(self) -> GetResponseType:
        return self._session.get('time/timerule')
