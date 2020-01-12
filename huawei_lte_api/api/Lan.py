from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class Lan(ApiGroup):
    def host_info(self) -> GetResponseType:
        return self._connection.get('lan/HostInfo')
