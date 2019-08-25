from collections import OrderedDict
from huawei_lte_api.ApiGroup import ApiGroup


class Security(ApiGroup):

    def bridgemode(self) -> dict:
        return self._connection.get('security/bridgemode')

    def get_firewall_switch(self) -> dict:
        return self._connection.get('security/firewall-switch')

    def set_firewall_switch(self,
                            firewall: bool=True,
                            ip_filter: bool=False,
                            wan_ping_filter: bool=True,
                            url_filter: bool=False,
                            mac_filter: bool=False
                            ) -> dict:
        return self._connection.post('security/firewall-switch', OrderedDict((
            ('FirewallMainSwitch', int(firewall)),
            ('FirewallIPFilterSwitch', int(ip_filter)),
            ('FirewallWanPortPingSwitch', int(wan_ping_filter)),
            ('firewallurlfilterswitch', int(url_filter)),
            ('firewallmacfilterswitch', int(mac_filter))
        )))

    def mac_filter(self) -> dict:
        return self._connection.get('security/mac-filter')

    def lan_ip_filter(self) -> dict:
        return self._connection.get('security/lan-ip-filter')

    def virtual_servers(self) -> dict:
        return self._connection.get('security/virtual-servers')

    def url_filter(self) -> dict:
        return self._connection.get('security/url-filter')

    def upnp(self) -> dict:
        return self._connection.get('security/upnp')

    def set_upnp(self, enabled: bool):
        return self._connection.post('security/upnp', {
            'UpnpStatus': int(enabled),
        })

    def dmz(self) -> dict:
        return self._connection.get('security/dmz')

    def set_dmz(self, enabled: bool, ip_address: str):
        return self._connection.post('security/dmz', OrderedDict((
            ('DmzStatus', int(enabled)),
            ('DmzIPAddress', ip_address)
        )))

    def sip(self) -> dict:
        return self._connection.get('security/sip')

    def set_sip(self, enabled: bool, port: int):
        return self._connection.post('security/sip', OrderedDict((
            ('SipStatus', int(enabled)),
            ('SipPort', port)
        )))

    def feature_switch(self) -> dict:
        return self._connection.get('security/feature-switch')

    def nat(self) -> dict:
        return self._connection.get('security/nat')

    def special_applications(self) -> dict:
        return self._connection.get('security/special-applications')

    def white_lan_ip_filter(self) -> dict:
        return self._connection.get('security/white-lan-ip-filter')

    def white_url_filter(self) -> dict:
        return self._connection.get('security/white-url-filter')
