from collections import OrderedDict
from huawei_lte_api.ApiGroup import ApiGroup


class Net(ApiGroup):
    def current_plmn(self) -> dict:
        return self._connection.get('net/current-plmn')

    def net_mode(self) -> dict:
        return self._connection.get('net/net-mode')

    def set_net_mode(self, lteband: str, networkband: str, networkmode: str):
        return self._connection.post('net/net-mode', OrderedDict((
            ('NetworkMode', networkmode),
            ('NetworkBand', networkband),
            ('LTEBand', lteband)
        )))

    def network(self) -> dict:
        return self._connection.get('net/network')

    def register(self) -> dict:
        return self._connection.get('net/register')

    def net_mode_list(self) -> dict:
        return self._connection.get('net/net-mode-list')

    def plmn_list(self) -> dict:
        """
    !FIXME LOL DoS! no auth required :-D
    :return:
    """
        return self._connection.get('net/plmn-list')

    def net_feature_switch(self) -> dict:
        return self._connection.get('net/net-feature-switch')

    def cell_info(self) -> dict:
        return self._connection.get('net/cell-info')

    def csps_state(self) -> dict:
        return self._connection.get('net/csps_state')
