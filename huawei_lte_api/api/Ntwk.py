from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Ntwk(ApiGroup):

    def lan_upnp_portmapping(self) -> GetResponseType:
        return self._session.get('ntwk/lan_upnp_portmapping')

    def celllock(self) -> GetResponseType:
        return self._session.get('ntwk/celllock')

    def dualwaninfo(self) -> GetResponseType:
        return self._session.get('ntwk/dualwaninfo')
