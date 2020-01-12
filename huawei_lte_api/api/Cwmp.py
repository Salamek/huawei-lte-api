from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class Cwmp(ApiGroup):
    def basic_info(self) -> GetResponseType:
        return self._connection.get('cwmp/basic-info')
