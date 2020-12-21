from collections import OrderedDict
from typing import Union
from huawei_lte_api.enums.net import NetworkModeEnum
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType, SetResponseType


ALL_BANDS = '7fffffffffffffff'


class Net(ApiGroup):
    def current_plmn(self) -> GetResponseType:
        return self._connection.get('net/current-plmn')

    def net_mode(self) -> GetResponseType:
        return self._connection.get('net/net-mode')

    def set_net_mode(self, lteband: str, networkband: str, networkmode: Union[NetworkModeEnum, str]) -> SetResponseType:
        """
        :param lteband: bitmask of per band ints or'd together, where each band N is represented as 2**(N-1), in hex
            without leading '0x'. For example B1,B3,B20: hex(2**(1-1) | 2**(3-1) | 2**(20-1))[2:] = '80005'.
            Use ALL_BANDS to indicate all bands. All values or combinations of them may not be supported.
        :param networkband:
        :param networkmode: network mode, see NetworkModeEnum; str supported for deprecated backwards compatiblity
        :return:
        """
        return self._connection.post_set('net/net-mode', OrderedDict((
            ('NetworkMode', networkmode if isinstance(networkmode, str) else networkmode.value),
            ('NetworkBand', networkband),
            ('LTEBand', lteband)
        )))

    def network(self) -> GetResponseType:
        return self._connection.get('net/network')

    def register(self) -> GetResponseType:
        return self._connection.get('net/register')

    def set_register(self, mode: str, plmn: str, rat: str) -> SetResponseType:
        """
        Sets network selection
        :param mode: "1": manual network selection, "0": auto
        :param plmn: Plmn code ("Numeric" value returned by net_mode_list()),
            "" for auto
        :param rat: "0": "2G", "2": "3G", "7": "4G" ("Rat" value returned by
            net_mode_list()), "" for auto
        :return: str
        """
        return self._connection.post_set('net/register', OrderedDict((
            ('Mode', mode),
            ('Plmn', plmn),
            ('Rat', rat)
        )))

    def net_mode_list(self) -> GetResponseType:
        return self._connection.get('net/net-mode-list')

    def plmn_list(self) -> GetResponseType:
        """
    !FIXME LOL DoS! no auth required :-D
    :return:
    """
        return self._connection.get('net/plmn-list')

    def net_feature_switch(self) -> GetResponseType:
        return self._connection.get('net/net-feature-switch')

    def cell_info(self) -> GetResponseType:
        return self._connection.get('net/cell-info')

    def csps_state(self) -> GetResponseType:
        return self._connection.get('net/csps_state')
