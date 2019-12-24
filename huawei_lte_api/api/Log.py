from huawei_lte_api.ApiGroup import ApiGroup, GetResponseType


class Log(ApiGroup):

    def loginfo(self) -> GetResponseType:
        return self._connection.get('log/loginfo')
