from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType
from huawei_lte_api.Tools import Tools


class Lan(ApiGroup):
    def host_info(self) -> GetResponseType:
        hosts = self._session.get('lan/HostInfo')
        # Make sure Hosts->Host is a list
        # It may be returned as a single dict if only one is associated,
        # as well as sometimes None.
        return Tools.enforce_list_response(hosts, 'Host')
