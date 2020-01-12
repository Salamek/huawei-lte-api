from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class TimeRule(ApiGroup):

    def timerule(self) -> GetResponseType:
        return self._connection.get('time/timerule')
