from huawei_lte_api.ApiGroup import ApiGroup, GetResponseType


class Time(ApiGroup):

    def timeout(self) -> GetResponseType:
        return self._connection.get('time/timeout')
