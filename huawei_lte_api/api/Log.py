from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class Log(ApiGroup):

    def loginfo(self) -> GetResponseType:
        return self._connection.get('log/loginfo')
