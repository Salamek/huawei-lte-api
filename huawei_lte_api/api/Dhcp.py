from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from huawei_lte_api.ApiGroup import ApiGroup

if TYPE_CHECKING:
    from collections.abc import Mapping

    from huawei_lte_api.Session import GetResponseType, SetResponseType


@dataclass
class DhcpSettings:
    """DHCP configuration with full lease range addresses and lease time in seconds."""

    dhcp_ip_address: str = "192.168.0.1"
    dhcp_lan_netmask: str = "255.255.255.0"
    dhcp_status: bool = True
    dhcp_start_ip_address: str = "192.168.0.100"
    dhcp_end_ip_address: str = "192.168.0.200"
    dhcp_lease_time: int = 86400
    dns_status: bool | None = True
    primary_dns: str | None = None
    secondary_dns: str | None = None
    show_dns_setting: bool | None = True

    @classmethod
    def from_dict(cls, data: Mapping[str, str | None]) -> DhcpSettings:
        def required_text(key: str) -> str:
            value = data[key]
            if not isinstance(value, str):
                msg = f"Expected text for DHCP setting {key}"
                raise TypeError(msg)
            return value

        return cls(
            dhcp_ip_address=required_text("DhcpIPAddress"),
            dhcp_lan_netmask=required_text("DhcpLanNetmask"),
            dhcp_status=required_text("DhcpStatus") == "1",
            dhcp_start_ip_address=required_text("DhcpStartIPAddress"),
            dhcp_end_ip_address=required_text("DhcpEndIPAddress"),
            dhcp_lease_time=int(required_text("DhcpLeaseTime")),
            dns_status=data["DnsStatus"] == "1" if "DnsStatus" in data else None,
            primary_dns=data.get("PrimaryDns"),
            secondary_dns=data.get("SecondaryDns"),
            show_dns_setting=data["ShowDnsSetting"] == "1" if "ShowDnsSetting" in data else None,
        )

    def to_dict(self) -> dict[str, str | None]:
        data: dict[str, str | None] = {
            "DhcpIPAddress": self.dhcp_ip_address,
            "DhcpLanNetmask": self.dhcp_lan_netmask,
            "DhcpStatus": "1" if self.dhcp_status else "0",
            "DhcpStartIPAddress": self.dhcp_start_ip_address,
            "DhcpEndIPAddress": self.dhcp_end_ip_address,
            "DhcpLeaseTime": str(self.dhcp_lease_time),
        }
        if self.dns_status is not None:
            data["DnsStatus"] = "1" if self.dns_status else "0"
        data["PrimaryDns"] = self.primary_dns
        data["SecondaryDns"] = self.secondary_dns
        if self.show_dns_setting is not None:
            data["ShowDnsSetting"] = "1" if self.show_dns_setting else "0"
        return data


class Dhcp(ApiGroup):
    def settings(self) -> DhcpSettings:
        """
        Get DHCP settings.

        :return: DHCP settings.

        Usage example:
        >>> dhcp = Dhcp(session)
        >>> settings = dhcp.settings()
        >>> print(settings)
        """
        return DhcpSettings.from_dict(self._session.get("dhcp/settings"))

    def feature_switch(self) -> GetResponseType:
        """
        Get DHCP feature switch status.

        :return: DHCP feature switch status.

        Usage example:
        >>> dhcp = Dhcp(session)
        >>> feature_switch = dhcp.feature_switch()
        >>> print(feature_switch)
        """
        return self._session.get("dhcp/feature-switch")

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
        return self._session.get("dhcp/dhcp-host-info")

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
        return self._session.get("dhcp/static-addr-info")

    def set_settings(self, settings: DhcpSettings) -> SetResponseType:
        """Write DHCP settings to the router.

        Pass a DhcpSettings instance in place of the former keyword arguments.
        Edit a configuration returned by settings() to keep its other known
        fields, or construct DhcpSettings with defaults for a new configuration.
        """
        return self._session.post_set("dhcp/settings", settings.to_dict())
