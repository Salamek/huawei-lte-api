from typing import cast
from unittest.mock import Mock

from huawei_lte_api.api.Dhcp import Dhcp, DhcpSettings
from huawei_lte_api.Session import Session

SETTINGS = {
    "DhcpStatus": "1",
    "DhcpIPAddress": "192.168.0.1",
    "DhcpLanNetmask": "255.255.255.0",
    "DhcpStartIPAddress": "192.168.0.100",
    "DhcpEndIPAddress": "192.168.0.200",
    "DhcpLeaseTime": "86400",
}


def test_read_edit_write_sends_only_known_fields() -> None:
    session = Mock(spec=Session)
    data = {**SETTINGS, "PrimaryDns": None, "FirmwareOption": "custom"}
    session.get.return_value = data
    session.post_set.return_value = "OK"
    dhcp = Dhcp(cast("Session", session))

    settings = dhcp.settings()
    assert settings.dhcp_status is True
    assert settings.dhcp_lease_time == 86400
    assert settings.dhcp_start_ip_address == "192.168.0.100"
    session.post_set.assert_not_called()

    settings.dhcp_status = False
    settings.dhcp_lease_time = 3600
    assert dhcp.set_settings(settings) == "OK"

    session.get.assert_called_once_with("dhcp/settings")
    session.post_set.assert_called_once_with(
        "dhcp/settings",
        {**SETTINGS, "DhcpStatus": "0", "DhcpLeaseTime": "3600", "PrimaryDns": None, "SecondaryDns": None},
    )
    assert data == {**SETTINGS, "PrimaryDns": None, "FirmwareOption": "custom"}


def test_write_constructed_settings_does_not_read_router() -> None:
    session = Mock(spec=Session)
    dhcp = Dhcp(cast("Session", session))

    dhcp.set_settings(DhcpSettings(primary_dns="1.1.1.1"))

    session.get.assert_not_called()
    session.post_set.assert_called_once_with(
        "dhcp/settings",
        {**SETTINGS, "DnsStatus": "1", "PrimaryDns": "1.1.1.1", "SecondaryDns": None, "ShowDnsSetting": "1"},
    )
