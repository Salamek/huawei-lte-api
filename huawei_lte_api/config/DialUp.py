from huawei_lte_api.ApiGroup import ApiGroup


class DialUp(ApiGroup):
    def config(self):
        return self._connection.get('dialup/config.xml', prefix='config')

    def connectmode(self):
        return self._connection.get('dialup/connectmode.xml', prefix='config')
