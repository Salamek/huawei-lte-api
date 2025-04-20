from typing import Optional
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType, SetResponseType


class Dhcp(ApiGroup):
    def settings(self) -> GetResponseType:
        """
        Get DHCP settings.

        :return: DHCP settings.

        Usage example:
        >>> dhcp = Dhcp(session)
        >>> settings = dhcp.settings()
        >>> print(settings)
        """
        return self._session.get('dhcp/settings')

    def feature_switch(self) -> GetResponseType:
        """
        Get DHCP feature switch status.

        :return: DHCP feature switch status.

        Usage example:
        >>> dhcp = Dhcp(session)
        >>> feature_switch = dhcp.feature_switch()
        >>> print(feature_switch)
        """
        return self._session.get('dhcp/feature-switch')

    def dhcp_host_info(self) -> GetResponseType:
        """
        Get DHCP host information.

        Endpoint found by reverse engineering B310s-22 firmware, unknown usage.

        :return: DHCP host information.

        Usage example:
        >>> dhcp = Dhcp(session)
        >>> host_info = dhcp.dhcp_host_info()
        >>> print(host_info)
        """
        return self._session.get('dhcp/dhcp-host-info')

    def static_addr_info(self) -> GetResponseType:
        """
        Get static address information.

        Endpoint found by reverse engineering B310s-22 firmware, unknown usage.

        :return: Static address information.

        Usage example:
        >>> dhcp = Dhcp(session)
        >>> static_info = dhcp.static_addr_info()
        >>> print(static_info)
        """
        return self._session.get('dhcp/static-addr-info')

    def set_settings(  # pylint: disable=too-many-arguments
        self,
        dhcp_ip_address: str = "192.168.0.1",
        dhcp_lan_netmask: str = "255.255.255.0",
        dhcp_status: bool = True,
        dhcp_start_ip_range: int = 100,
        dhcp_end_ip_range: int = 200,
        dhcp_lease_time: int = 86400,
        dns_status: bool = True,
        primary_dns: Optional[str] = None,
        secondary_dns: Optional[str] = None,
        show_dns_setting: bool = True,
    ) -> SetResponseType:
        """
        Configure DHCP server settings.

        :param dhcp_ip_address: IP address of DHCP server.
        :param dhcp_lan_netmask: Netmask for DHCP server.
        :param dhcp_status: Turn DHCP server on/off.
        :param dhcp_start_ip_range: Lease IP range from.
        :param dhcp_end_ip_range: Lease IP range till.
        :param dhcp_lease_time: IP lease duration.
        :param dns_status: DNS status.
        :param primary_dns: Primary DNS server IP.
        :param secondary_dns: Secondary DNS server IP.
        :param show_dns_setting: Show DNS setting.
        :return: Set response type.

        Usage example:
        >>> dhcp = Dhcp(session)
        >>> response = dhcp.set_settings(
        >>>     dhcp_ip_address="192.168.1.1", 
        >>>     dhcp_lan_netmask="255.255.255.0", 
        >>>     dhcp_status=True, 
        >>>     dhcp_start_ip_range=50, 
        >>>     dhcp_end_ip_range=150, 
        >>>     dhcp_lease_time=3600, 
        >>>     dns_status=True, 
        >>>     primary_dns="8.8.8.8", 
        >>>     secondary_dns="8.8.4.4", 
        >>>     show_dns_setting=True
        >>> )
        >>> print(response)
        """

        ip_address_parts = dhcp_ip_address.split(".")
        ip_address_parts.pop(-1)
        dhcp_start_ip_address = ".".join(ip_address_parts) + "." + str(dhcp_start_ip_range)
        dhcp_end_ip_address = ".".join(ip_address_parts) + "." + str(dhcp_end_ip_range)

        return self._session.post_set(
            'dhcp/settings',
            {
                'DhcpIPAddress': dhcp_ip_address,
                'DhcpLanNetmask': dhcp_lan_netmask,
                'DhcpStatus': 1 if dhcp_status else 0,
                'DhcpStartIPAddress': dhcp_start_ip_address,
                'DhcpEndIPAddress': dhcp_end_ip_address,
                'DhcpLeaseTime': dhcp_lease_time,
                'DnsStatus': 1 if dns_status else 0,
                'PrimaryDns': primary_dns,
                'SecondaryDns': secondary_dns,
                'ShowDnsSetting': 1 if show_dns_setting else 0,
            }
        )
