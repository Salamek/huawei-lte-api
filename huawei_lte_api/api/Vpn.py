from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Vpn(ApiGroup):

    def feature_switch(self) -> GetResponseType:
        return self._session.get('vpn/feature-switch')

    def br_list(self) -> GetResponseType:
        return self._session.get('vpn/br_list')

    def ipsec_settings(self) -> GetResponseType:
        return self._session.get('vpn/ipsec_settings')

    def l2tp_settings(self) -> GetResponseType:
        return self._session.get('vpn/l2tp_settings')

    def pptp_settings(self) -> GetResponseType:
        return self._session.get('vpn/pptp_settings')

    def status(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._session.get('vpn/status')
