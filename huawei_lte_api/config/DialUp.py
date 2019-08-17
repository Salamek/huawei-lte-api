from huawei_lte_api.ApiGroup import ApiGroup


class DialUp(ApiGroup):
    def config(self):
        return self._connection.get('dialup/config.xml', prefix='config')

    def connectmode(self):
        return self._connection.get('dialup/connectmode.xml', prefix='config')

    def profileswitch(self):
        return self._connection.get('dialup/profileswitch.xml', prefix='config')
