from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class Network(ApiGroup):
    def net_mode(self) -> GetResponseType:
        return self._connection.get('network/net-mode.xml', prefix='config')

    def networkmode(self) -> GetResponseType:
        return self._connection.get('network/networkmode.xml', prefix='config')

    def config(self) -> GetResponseType:
        return self._connection.get('network/config.xml', prefix='config')

    def networkband_null(self) -> GetResponseType:
        return self._connection.get('network/networkband_null.xml', prefix='config')

    def set_only_4g(self) -> GetResponseType:
        return self._connection.get('network/setOnly4g.xml', prefix='config')
