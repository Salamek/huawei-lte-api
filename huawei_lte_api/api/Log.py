from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Log(ApiGroup):

    def loginfo(self) -> GetResponseType:
        return self._session.get('log/loginfo')
