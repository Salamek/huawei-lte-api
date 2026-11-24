from __future__ import annotations

from typing import cast
from unittest.mock import Mock

from huawei_lte_api.api.Dhcp import Dhcp
from huawei_lte_api.Session import Session

SETTINGS = {
    "DhcpStatus": "0",
    "DhcpIPAddress": "192.168.0.1",
    "DhcpLanNetmask": "255.255.255.0",
    "DhcpStartIPAddress": "192.168.0.100",
    "DhcpEndIPAddress": "192.168.0.200",
    "DhcpLeaseTime": "86400",
    "DnsStatus": "1",
    "PrimaryDns": "1.1.1.1",
    "SecondaryDns": "8.8.8.8",
}


def make_dhcp() -> tuple[Dhcp, Mock]:
    session_mock = Mock(spec=Session)
    session_mock.get.return_value = SETTINGS.copy()
    session_mock.post_set.return_value = "OK"
    return Dhcp(cast("Session", session_mock)), session_mock


def test_set_status_enables_without_changing_other_settings() -> None:
    dhcp, session = make_dhcp()

    assert dhcp.set_status(True) == "OK"

    session.post_set.assert_called_once_with("dhcp/settings", {**SETTINGS, "DhcpStatus": "1"})


def test_set_status_disables_without_changing_other_settings() -> None:
    dhcp, session = make_dhcp()

    assert dhcp.set_status(False) == "OK"

    session.post_set.assert_called_once_with("dhcp/settings", {**SETTINGS, "DhcpStatus": "0"})
