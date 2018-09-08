from huawei_lte_api.ApiGroup import ApiGroup


class Log(ApiGroup):

    def loginfo(self) -> dict:
        return self._connection.get('log/loginfo')
