from collections import OrderedDict
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType, SetResponseType


class Net(ApiGroup):
    def current_plmn(self) -> GetResponseType:
        return self._connection.get('net/current-plmn')

    def net_mode(self) -> GetResponseType:
        return self._connection.get('net/net-mode')

    def set_net_mode(self, lteband: str, networkband: str, networkmode: str) -> SetResponseType:
        return self._connection.post_set('net/net-mode', OrderedDict((
            ('NetworkMode', networkmode),
            ('NetworkBand', networkband),
            ('LTEBand', lteband)
        )))

    def network(self) -> GetResponseType:
        return self._connection.get('net/network')

    def register(self) -> GetResponseType:
        return self._connection.get('net/register')

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
