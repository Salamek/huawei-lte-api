from huawei_lte_api.ApiGroup import ApiGroup


class Ntwk(ApiGroup):

    def lan_upnp_portmapping(self) -> dict:
        return self._connection.get('ntwk/lan_upnp_portmapping')
