from huawei_lte_api.ApiGroup import ApiGroup


class Wifi(ApiGroup):
    def configure(self):
        return self._connection.get('wifi/configure.xml', prefix='config')

    def country_channel(self):
        return self._connection.get('wifi/countryChannel.xml', prefix='config')
