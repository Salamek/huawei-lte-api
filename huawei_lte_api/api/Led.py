from huawei_lte_api.ApiGroup import ApiGroup


class Led(ApiGroup):
    def nightmode(self) -> dict:
        return self._connection.get('led/nightmode')
