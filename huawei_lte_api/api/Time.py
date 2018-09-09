from huawei_lte_api.ApiGroup import ApiGroup


class Time(ApiGroup):

    def timeout(self) -> dict:
        return self._connection.get('time/timeout')
