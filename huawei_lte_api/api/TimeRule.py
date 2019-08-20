from huawei_lte_api.ApiGroup import ApiGroup


class TimeRule(ApiGroup):

    def timerule(self) -> dict:
        return self._connection.get('time/timerule')
