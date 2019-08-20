from huawei_lte_api.ApiGroup import ApiGroup


class Network(ApiGroup):
    def net_mode(self):
        return self._connection.get('network/net-mode.xml', prefix='config')

    def networkmode(self):
        return self._connection.get('network/networkmode.xml', prefix='config')

    def config(self):
        return self._connection.get('network/config.xml', prefix='config')

    def networkband_null(self):
        return self._connection.get('network/networkband_null.xml', prefix='config')
