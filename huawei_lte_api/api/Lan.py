from huawei_lte_api.ApiGroup import ApiGroup


class Lan(ApiGroup):
    def host_info(self) -> dict:
        return self._connection.get('lan/HostInfo')
