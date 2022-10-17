from collections import OrderedDict

from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType, SetResponseType


class Security(ApiGroup):

    def bridgemode(self) -> GetResponseType:
        return self._session.get('security/bridgemode')

    def get_firewall_switch(self) -> GetResponseType:
        return self._session.get('security/firewall-switch')

    def set_firewall_switch(self,
                            firewall: bool = True,
                            ip_filter: bool = False,
                            wan_ping_filter: bool = True,
                            url_filter: bool = False,
                            mac_filter: bool = False
                            ) -> SetResponseType:
        return self._session.post_set('security/firewall-switch', OrderedDict((
            ('FirewallMainSwitch', int(firewall)),
            ('FirewallIPFilterSwitch', int(ip_filter)),
            ('FirewallWanPortPingSwitch', int(wan_ping_filter)),
            ('firewallurlfilterswitch', int(url_filter)),
            ('firewallmacfilterswitch', int(mac_filter))
        )))

    def mac_filter(self) -> GetResponseType:
        return self._session.get('security/mac-filter')

    def lan_ip_filter(self) -> GetResponseType:
        return self._session.get('security/lan-ip-filter')

    def virtual_servers(self) -> GetResponseType:
        return self._session.get('security/virtual-servers')

    def url_filter(self) -> GetResponseType:
        return self._session.get('security/url-filter')

    def set_url_filter(self, urlfilters: GetResponseType) -> SetResponseType:
        """
        :param urlfilters: same structure as `url_filter` return value
        """
        return self._session.post_set('security/url-filter', urlfilters)

    def upnp(self) -> GetResponseType:
        return self._session.get('security/upnp')

    def set_upnp(self, enabled: bool) -> SetResponseType:
        return self._session.post_set('security/upnp', {
            'UpnpStatus': int(enabled),
        })

    def dmz(self) -> GetResponseType:
        return self._session.get('security/dmz')

    def set_dmz(self, enabled: bool, ip_address: str) -> SetResponseType:
        return self._session.post_set('security/dmz', OrderedDict((
            ('DmzStatus', int(enabled)),
            ('DmzIPAddress', ip_address)
        )))

    def sip(self) -> GetResponseType:
        return self._session.get('security/sip')

    def set_sip(self, enabled: bool, port: int) -> SetResponseType:
        return self._session.post_set('security/sip', OrderedDict((
            ('SipStatus', int(enabled)),
            ('SipPort', port)
        )))

    def feature_switch(self) -> GetResponseType:
        return self._session.get('security/feature-switch')

    def nat(self) -> GetResponseType:
        return self._session.get('security/nat')

    def special_applications(self) -> GetResponseType:
        return self._session.get('security/special-applications')

    def white_lan_ip_filter(self) -> GetResponseType:
        return self._session.get('security/white-lan-ip-filter')

    def white_url_filter(self) -> GetResponseType:
        return self._session.get('security/white-url-filter')

    def set_white_url_filter(self, urlfilters: GetResponseType) -> SetResponseType:
        """
        :param urlfilters: same structure as `white_url_filter` return value
        """
        return self._session.post_set('security/white-url-filter', urlfilters)

    def acls(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage, probably not implemented by Huawei
        :return:
        """
        return self._session.get('security/acls')
