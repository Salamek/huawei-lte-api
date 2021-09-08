from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Lan(ApiGroup):
    def host_info(self) -> GetResponseType:
        return self._session.get('lan/HostInfo')
