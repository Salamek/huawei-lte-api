from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class Led(ApiGroup):
    def nightmode(self) -> GetResponseType:
        return self._connection.get('led/nightmode')
