from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class DDns(ApiGroup):
    def get_ddns_list(self) -> GetResponseType:
        """
        Get the list of DDNS configurations.

        :return: List of DDNS configurations.

        Usage example:
        >>> ddns = DDns(session)
        >>> ddns_list = ddns.get_ddns_list()
        >>> print(ddns_list)
        """
        return self._session.get('ddns/ddns-list')

    def get_status(self) -> GetResponseType:
        """
        Get the status of DDNS.

        :return: DDNS status.

        Usage example:
        >>> ddns = DDns(session)
        >>> status = ddns.get_status()
        >>> print(status)
        """
        return self._session.get('ddns/status')

    def serverlist(self) -> GetResponseType:
        """
        Get the list of DDNS servers.

        :return: List of DDNS servers.

        Usage example:
        >>> ddns = DDns(session)
        >>> server_list = ddns.serverlist()
        >>> print(server_list)
        """
        return self._session.get('ddns/serverlist')
