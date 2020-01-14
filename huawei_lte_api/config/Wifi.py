from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class Wifi(ApiGroup):
    def config(self) -> GetResponseType:
        return self._connection.get('wifi/config.xml', prefix='config')

    def configure(self) -> GetResponseType:
        return self._connection.get('wifi/configure.xml', prefix='config')

    def country_channel(self) -> GetResponseType:
        return self._connection.get('wifi/countryChannel.xml', prefix='config')

    def channel_auto_match_hardware(self) -> GetResponseType:
        return self._connection.get('wifi/channelAutoMatchHardware.xml', prefix='config')
