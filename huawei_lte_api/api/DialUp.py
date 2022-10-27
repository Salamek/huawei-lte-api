from typing import Optional
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType, SetResponseType
from huawei_lte_api.enums.dialup import AuthModeEnum, IpType


class DialUp(ApiGroup):
    def mobile_dataswitch(self) -> GetResponseType:
        """
        Get current LTE modem toggle state
        :return:
        """
        return self._session.get('dialup/mobile-dataswitch')

    def connection(self) -> GetResponseType:
        return self._session.get('dialup/connection')

    def dialup_feature_switch(self) -> GetResponseType:
        return self._session.get('dialup/dialup-feature-switch')

    def profiles(self) -> GetResponseType:
        return self._session.get('dialup/profiles')

    def auto_apn(self) -> GetResponseType:
        return self._session.get('dialup/auto-apn')

    def dial(self) -> SetResponseType:
        return self._session.post_set('dialup/dial', {
            'Action': 1
        })

    def set_mobile_dataswitch(self, dataswitch: int = 0) -> SetResponseType:
        """
        Toggle LTE modem state
        :param dataswitch: 0 to disable LTE modem, 1 to enable LTE modem
        """
        return self._session.post_set('dialup/mobile-dataswitch', {
            'dataswitch': dataswitch
        })

    def set_default_profile(self, default: int = 0) -> SetResponseType:
        return self._session.post_set('dialup/profiles', {
            'SetDefault': default,
            'Delete': 0,
            'Modify': 0
        }, is_encrypted=True)

    def delete_profile(self, index: int) -> SetResponseType:
        return self._session.post_set('dialup/profiles', {
            'SetDefault': 0,
            'Delete': index,
            'Modify': 0
        }, is_encrypted=True)

    def create_profile(self,
                       name: str,
                       username: Optional[str] = None,
                       password: Optional[str] = None,
                       apn: Optional[str] = None,
                       dialup_number: Optional[str] = None,
                       auth_mode: AuthModeEnum = AuthModeEnum.AUTO,
                       ip_type: IpType = IpType.IPV4_IPV6,
                       is_default: bool = False
                       ) -> SetResponseType:
        return self._session.post_set('dialup/profiles', {
            'SetDefault': 1 if is_default else 0,
            'Delete': 0,
            'Modify': 1,
            'Profile': {
                'Index': '',
                'IsValid': 1,
                'Name': name,
                'ApnIsStatic': 1 if apn else 0,
                'ApnName': apn,
                'DialupNum': dialup_number,
                'Username': username,
                'Password': password,
                'AuthMode': auth_mode.value,
                'IpIsStatic': '',
                'IpAddress': '',
                'DnsIsStatic': '',
                'PrimaryDns': '',
                'SecondaryDns': '',
                'ReadOnly': '0',
                'iptype': ip_type.value
            }
        }, is_encrypted=True)

    def set_connection_settings(
        self,
        roam_auto_connect_enable: bool = True,
        max_idle_time: int = 0,
        connect_mode: int = 0,
        mtu: int = 1500,
        auto_dial_switch: bool = True,
        pdp_always_on: bool = True,
    ) -> SetResponseType:
        """
        Set connection settings.
        :param roam_auto_connect_enable: Enable/Disable data roaming.
        :param max_idle_time: Auto disconnect interval, 0 is always on.
        :param connect_mode: Unknown usage.
        :param mtu: Unknown usage.
        :param auto_dial_switch: Unknown usage.
        :param pdp_always_on: Unknown usage.
        :return SetResponseType: Set response type.
        """

        return self._session.post_set(
            'dialup/connection',
            {
                'RoamAutoConnectEnable': 1 if roam_auto_connect_enable else 0,
                'MaxIdelTime': max_idle_time,
                'ConnectMode': connect_mode,
                'MTU': mtu,
                'auto_dial_switch': 1 if auto_dial_switch else 0,
                'pdp_always_on': 1 if pdp_always_on else 0,
            }
        )
