from huawei_lte_api.ApiGroup import ApiGroup


class Wifi(ApiGroup):
    def configure(self):
        return self._connection.get('wifi/configure.xml', prefix='config')

    def country_channel(self):
        return self._connection.get('wifi/countryChannel.xml', prefix='config')

    def channel_auto_match_hardware(self):
        return self._connection.get('wifi/channelAutoMatchHardware.xml', prefix='config')
