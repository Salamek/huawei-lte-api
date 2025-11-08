from collections import OrderedDict
from typing import Union

from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType, SetResponseType
from huawei_lte_api.enums.net import NetworkModeEnum


class Net(ApiGroup):
    def current_plmn(self) -> GetResponseType:
        """
        Get the current Public Land Mobile Network (PLMN).

        :return: Current PLMN information.

        Usage example:
        >>> net = Net(session)
        >>> current_plmn = net.current_plmn()
        >>> print(current_plmn)
        """
        return self._session.get('net/current-plmn')

    def net_mode(self) -> GetResponseType:
        """
        Get the current network mode.

        :return: Current network mode.

        Usage example:
        >>> net = Net(session)
        >>> net_mode = net.net_mode()
        >>> print(net_mode)
        """
        return self._session.get('net/net-mode')

    def set_net_mode(self, lteband: Union[str, int], networkband: Union[int, str], networkmode: Union[NetworkModeEnum, str]) -> SetResponseType:
        """
        Set the network mode.

        :param lteband: Bitmask of LTE band ints or'd together, where each band N is represented as 2**(N-1), as int,
            or hex str without leading '0x'. For example B1,B3,B20: 2**(1-1) | 2**(3-1) | 2**(20-1) = 0x80005.
            Use ALL for all or when not applicable (not 4G mode). All values or combinations of them may not be
            supported.
        :param networkband: Bitmask of 3G network band ints or'd together, as int, or hex str without leading '0x'.
            See NetworkBandEnum, use ALL for all or when not applicable (not 3G mode). All values or combinations
            of them may not be supported.
        :param networkmode: Network mode, see NetworkModeEnum; str supported for deprecated backwards compatibility.
        :return: Set response type.

        Usage example:
        >>> net = Net(session)
        >>> response = net.set_net_mode(lteband=0x80005, networkband=0x3fffffff, networkmode=NetworkModeEnum.MODE_AUTO)
        >>> print(response)
        """
        return self._session.post_set('net/net-mode', OrderedDict((
            ('NetworkMode', networkmode if isinstance(networkmode, str) else networkmode.value),
            ('NetworkBand', networkband if isinstance(networkband, str) else f'{networkband:x}'),
            ('LTEBand', lteband if isinstance(lteband, str) else f'{lteband:x}'),
        )))

    def network(self) -> GetResponseType:
        """
        Get the network information.

        :return: Network information.

        Usage example:
        >>> net = Net(session)
        >>> network_info = net.network()
        >>> print(network_info)
        """
        return self._session.get('net/network')

    def set_network(self, networkmode: str, networkband: str) -> SetResponseType:
        """
        Set the network mode and band.

        :param networkmode: Different value range than in net_mode/NetworkModeEnum.
        :param networkband: Different value range than in net_mode.
        :return: Set response type.

        Usage example:
        >>> net = Net(session)
        >>> response = net.set_network(networkmode="03", networkband="3fffffff")
        >>> print(response)
        """
        return self._session.post_set('net/network', OrderedDict((
            ('NetworkMode', networkmode),
            ('NetworkBand', networkband),
        )))

    def register(self) -> GetResponseType:
        """
        Get the network registration status.

        :return: Network registration status.

        Usage example:
        >>> net = Net(session)
        >>> registration_status = net.register()
        >>> print(registration_status)
        """
        return self._session.get('net/register')

    def set_register(self, mode: str, plmn: str, rat: str) -> SetResponseType:
        """
        Set the network registration mode.

        :param mode: "1": manual network selection, "0": auto.
        :param plmn: PLMN code ("Numeric" value returned by net_mode_list()), "" for auto.
        :param rat: "0": "2G", "2": "3G", "7": "4G" ("Rat" value returned by net_mode_list()), "" for auto.
        :return: Set response type.

        Usage example:
        >>> net = Net(session)
        >>> response = net.set_register(mode="1", plmn="12345", rat="7")
        >>> print(response)
        """
        return self._session.post_set('net/register', OrderedDict((
            ('Mode', mode),
            ('Plmn', plmn),
            ('Rat', rat)
        )))

    def net_mode_list(self) -> GetResponseType:
        """
        Get the list of available network modes.

        :return: List of available network modes.

        Usage example:
        >>> net = Net(session)
        >>> net_mode_list = net.net_mode_list()
        >>> print(net_mode_list)
        """
        return self._session.get('net/net-mode-list')

    def plmn_list(self) -> GetResponseType:
        """
        Get the list of available PLMNs.

        :return: List of available PLMNs.

        Usage example:
        >>> net = Net(session)
        >>> plmn_list = net.plmn_list()
        >>> print(plmn_list)
        """
        return self._session.get('net/plmn-list')

    def net_feature_switch(self) -> GetResponseType:
        """
        Get the status of the network feature switch.

        :return: Network feature switch status.

        Usage example:
        >>> net = Net(session)
        >>> feature_switch_status = net.net_feature_switch()
        >>> print(feature_switch_status)
        """
        return self._session.get('net/net-feature-switch')

    def cell_info(self) -> GetResponseType:
        """
        Get the cell information.

        :return: Cell information.

        Usage example:
        >>> net = Net(session)
        >>> cell_info = net.cell_info()
        >>> print(cell_info)
        """
        return self._session.get('net/cell-info')

    def csps_state(self) -> GetResponseType:
        """
        Get the CSPS state.

        :return: CSPS state.

        Usage example:
        >>> net = Net(session)
        >>> csps_state = net.csps_state()
        >>> print(csps_state)
        """
        return self._session.get('net/csps_state')

    def reconnect(self) -> SetResponseType:
        """
        Reconnect to the network.

        :return: Set response type.

        Usage example:
        >>> net = Net(session)
        >>> response = net.reconnect()
        >>> print(response)
        """
        return self._session.post_set('net/reconnect', OrderedDict((
            ('ReconnectAction', 1),
        )))
