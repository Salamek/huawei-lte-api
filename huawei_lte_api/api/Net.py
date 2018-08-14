
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class Net(ApiGroup):
    def current_plmn(self) -> dict:
        return self._connection.get('net/current-plmn')

    def net_mode(self) -> dict:
        return self._connection.get('net/net-mode')

    @authorized_call
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