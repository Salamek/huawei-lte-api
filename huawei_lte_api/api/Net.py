
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class Net(ApiGroup):
    def current_plmn(self):
        return self._connection.get('net/current-plmn')

    def net_mode(self):
        return self._connection.get('net/net-mode')

    @authorized_call
    def network(self):
        return self._connection.get('net/network')

    def register(self):
        return self._connection.get('net/register')

    def net_mode_list(self):
        return self._connection.get('net/net-mode-list')

    def plmn_list(self):
        """
    !FIXME LOL DoS! no auth required :-D
    :return:
    """
        return self._connection.get('net/plmn-list')

    def net_feature_switch(self):
        return self._connection.get('net/net-feature-switch')