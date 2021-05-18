from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class Lan(ApiGroup):
    def host_info(self) -> GetResponseType:
        # Make sure Hosts->Host is a list
        # It may be returned as a single dict if only one is associated,
        # as well as sometimes None.
        hosts = self._connection.get('lan/HostInfo')
        if hosts.get('Hosts') is None:
            hosts['Hosts'] = {}
        host = hosts['Hosts'].setdefault('Host', [])
        if isinstance(host, dict):
            hosts['Hosts']['Host'] = [host]
        return hosts
