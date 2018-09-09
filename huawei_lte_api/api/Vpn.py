from huawei_lte_api.ApiGroup import ApiGroup


class Vpn(ApiGroup):

    def feature_switch(self) -> dict:
        return self._connection.get('vpn/feature-switch')

    def br_list(self) -> dict:
        return self._connection.get('vpn/br_list')

    def ipsec_settings(self) -> dict:
        return self._connection.get('vpn/ipsec_settings')

    def l2tp_settings(self) -> dict:
        return self._connection.get('vpn/l2tp_settings')

    def pptp_settings(self) -> dict:
        return self._connection.get('vpn/pptp_settings')
