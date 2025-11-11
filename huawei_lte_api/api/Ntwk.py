from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Ntwk(ApiGroup):
    def lan_upnp_portmapping(self) -> GetResponseType:
        """
        Get the LAN UPnP port mapping.

        :return: LAN UPnP port mapping.

        Usage example:
        >>> ntwk = Ntwk(session)
        >>> lan_upnp_portmapping = ntwk.lan_upnp_portmapping()
        >>> print(lan_upnp_portmapping)
        """
        return self._session.get("ntwk/lan_upnp_portmapping")

    def celllock(self) -> GetResponseType:
        """
        Get the cell lock status.

        :return: Cell lock status.

        Usage example:
        >>> ntwk = Ntwk(session)
        >>> celllock_status = ntwk.celllock()
        >>> print(celllock_status)
        """
        return self._session.get("ntwk/celllock")

    def dualwaninfo(self) -> GetResponseType:
        """
        Get the dual WAN information.

        :return: Dual WAN information.

        Usage example:
        >>> ntwk = Ntwk(session)
        >>> dualwan_info = ntwk.dualwaninfo()
        >>> print(dualwan_info)
        """
        return self._session.get("ntwk/dualwaninfo")

    def lan_wan_config(self) -> GetResponseType:
        """
        Get the LAN/WAN configuration.

        :return: LAN/WAN configuration.

        Usage example:
        >>> ntwk = Ntwk(session)
        >>> lan_wan_config = ntwk.lan_wan_config()
        >>> print(lan_wan_config)
        """
        return self._session.get("ntwk/lan-wan-config")
