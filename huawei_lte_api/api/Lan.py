from huawei_lte_api.ApiGroup import ApiGroup, GetResponseType


class Lan(ApiGroup):
    def host_info(self) -> GetResponseType:
        return self._connection.get('lan/HostInfo')
