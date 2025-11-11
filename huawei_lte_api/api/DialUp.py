from typing import Optional

from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.enums.dialup import AuthModeEnum, IpType
from huawei_lte_api.Session import GetResponseType, SetResponseType


class DialUp(ApiGroup):
    def mobile_dataswitch(self) -> GetResponseType:
        """
        Get current LTE modem toggle state.

        :return: Current LTE modem toggle state.

        Usage example:
        >>> dialup = DialUp(session)
        >>> state = dialup.mobile_dataswitch()
        >>> print(state)
        """
        return self._session.get("dialup/mobile-dataswitch")

    def connection(self) -> GetResponseType:
        """
        Get connection settings.

        :return: Connection settings.

        Usage example:
        >>> dialup = DialUp(session)
        >>> connection_settings = dialup.connection()
        >>> print(connection_settings)
        """
        return self._session.get("dialup/connection")

    def dialup_feature_switch(self) -> GetResponseType:
        """
        Get dial-up feature switch status.

        :return: Dial-up feature switch status.

        Usage example:
        >>> dialup = DialUp(session)
        >>> feature_switch = dialup.dialup_feature_switch()
        >>> print(feature_switch)
        """
        return self._session.get("dialup/dialup-feature-switch")

    def profiles(self) -> GetResponseType:
        """
        Get dial-up profiles.

        :return: Dial-up profiles.

        Usage example:
        >>> dialup = DialUp(session)
        >>> profiles = dialup.profiles()
        >>> print(profiles)
        """
        return self._session.get("dialup/profiles")

    def auto_apn(self) -> GetResponseType:
        """
        Get auto APN settings.

        :return: Auto APN settings.

        Usage example:
        >>> dialup = DialUp(session)
        >>> auto_apn_settings = dialup.auto_apn()
        >>> print(auto_apn_settings)
        """
        return self._session.get("dialup/auto-apn")

    def dial(self) -> SetResponseType:
        """
        Initiate a dial-up connection.

        :return: Set response type.

        Usage example:
        >>> dialup = DialUp(session)
        >>> response = dialup.dial()
        >>> print(response)
        """
        return self._session.post_set("dialup/dial", {
            "Action": 1,
        })

    def set_mobile_dataswitch(self, dataswitch: int = 0) -> SetResponseType:
        """
        Toggle LTE modem state.

        :param dataswitch: 0 to disable LTE modem, 1 to enable LTE modem.
        :return: Set response type.

        Usage example:
        >>> dialup = DialUp(session)
        >>> response = dialup.set_mobile_dataswitch(dataswitch=1)
        >>> print(response)
        """
        return self._session.post_set("dialup/mobile-dataswitch", {
            "dataswitch": dataswitch,
        })

    def set_default_profile(self, index: int = 0) -> SetResponseType:
        """
        Set the default dial-up profile.

        :param index: Index of the profile to set as default.
        :return: Set response type.

        Usage example:
        >>> dialup = DialUp(session)
        >>> response = dialup.set_default_profile(index=1)
        >>> print(response)
        """
        return self._session.post_set("dialup/profiles", {
            "SetDefault": index,
            "Delete": 0,
            "Modify": 0,
        }, is_encrypted=True)

    def delete_profile(self, index: int) -> SetResponseType:
        """
        Delete a dial-up profile.

        :param index: Index of the profile to delete.
        :return: Set response type.

        Usage example:
        >>> dialup = DialUp(session)
        >>> response = dialup.delete_profile(index=1)
        >>> print(response)
        """
        return self._session.post_set("dialup/profiles", {
            "SetDefault": 0,
            "Delete": index,
            "Modify": 0,
        }, is_encrypted=True)

    def create_profile(self,
                       name: str,
                       username: Optional[str] = None,
                       password: Optional[str] = None,
                       apn: Optional[str] = None,
                       dialup_number: Optional[str] = None,
                       auth_mode: AuthModeEnum = AuthModeEnum.AUTO,
                       ip_type: IpType = IpType.IPV4_IPV6,
                       is_default: bool = False,
                       ) -> SetResponseType:
        """
        Create a new dial-up profile.

        :param name: Profile name.
        :param username: Username for the profile.
        :param password: Password for the profile.
        :param apn: APN for the profile.
        :param dialup_number: Dial-up number for the profile.
        :param auth_mode: Authentication mode for the profile.
        :param ip_type: IP type for the profile.
        :param is_default: Boolean indicating whether to set the profile as default.
        :return: Set response type.

        Usage example:
        >>> dialup = DialUp(session)
        >>> response = dialup.create_profile(
        >>>     name="NewProfile",
        >>>     username="user",
        >>>     password="pass",
        >>>     apn="internet",
        >>>     dialup_number="*99#",
        >>>     auth_mode=AuthModeEnum.PAP,
        >>>     ip_type=IpType.IPV4,
        >>>     is_default=True
        >>> )
        >>> print(response)
        """
        return self._session.post_set("dialup/profiles", {
            "SetDefault": 1 if is_default else 0, # For E5576, the new profile will always become the default (See #221)
            "Delete": 0,
            "Modify": 1,
            "Profile": {
                "Index": "",
                "IsValid": 1,
                "Name": name,
                "ApnIsStatic": 1 if apn else 0,
                "ApnName": apn,
                "DialupNum": dialup_number,
                "Username": username,
                "Password": password,
                "AuthMode": auth_mode.value,
                "IpIsStatic": "",
                "IpAddress": "",
                "DnsIsStatic": "",
                "PrimaryDns": "",
                "SecondaryDns": "",
                "ReadOnly": "0",
                "iptype": ip_type.value,
            },
        }, is_encrypted=True)

    def update_profile(self,
                       index: int,
                       name: str,
                       username: Optional[str] = None,
                       password: Optional[str] = None,
                       apn: Optional[str] = None,
                       dialup_number: Optional[str] = None,
                       auth_mode: AuthModeEnum = AuthModeEnum.AUTO,
                       ip_type: IpType = IpType.IPV4_IPV6,
                       is_default: bool = False,
                       ) -> SetResponseType:
        """
        Update an existing dial-up profile.

        :param index: Index of the profile to update.
        :param name: Profile name.
        :param username: Username for the profile.
        :param password: Password for the profile.
        :param apn: APN for the profile.
        :param dialup_number: Dial-up number for the profile.
        :param auth_mode: Authentication mode for the profile.
        :param ip_type: IP type for the profile.
        :param is_default: Boolean indicating whether to set the profile as default.
        :return: Set response type.

        Usage example:
        >>> dialup = DialUp(session)
        >>> response = dialup.update_profile(
        >>>     index=1,
        >>>     name="UpdatedProfile",
        >>>     username="user",
        >>>     password="pass",
        >>>     apn="internet",
        >>>     dialup_number="*99#",
        >>>     auth_mode=AuthModeEnum.PAP,
        >>>     ip_type=IpType.IPV4,
        >>>     is_default=True
        >>> )
        >>> print(response)
        """
        return self._session.post_set("dialup/profiles", {
            "SetDefault": index if is_default else 0,
            "Delete": 0,
            "Modify": 2,
            "Profile": {
                "Index": index,
                "IsValid": 1,
                "Name": name,
                "ApnIsStatic": 1 if apn else 0,
                "ApnName": apn,
                "DialupNum": dialup_number,
                "Username": username,
                "Password": password,
                "AuthMode": auth_mode.value,
                "IpIsStatic": "",
                "IpAddress": "",
                "DnsIsStatic": "",
                "PrimaryDns": "",
                "SecondaryDns": "",
                "ReadOnly": "0",
                "iptype": ip_type.value,
            },
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
        :return: Set response type.

        Usage example:
        >>> dialup = DialUp(session)
        >>> response = dialup.set_connection_settings(roam_auto_connect_enable=True, max_idle_time=0, connect_mode=0, mtu=1500, auto_dial_switch=True, pdp_always_on=True)
        >>> print(response)
        """
        return self._session.post_set(
            "dialup/connection",
            {
                "RoamAutoConnectEnable": 1 if roam_auto_connect_enable else 0,
                "MaxIdelTime": max_idle_time,
                "ConnectMode": connect_mode,
                "MTU": mtu,
                "auto_dial_switch": 1 if auto_dial_switch else 0,
                "pdp_always_on": 1 if pdp_always_on else 0,
            },
        )
