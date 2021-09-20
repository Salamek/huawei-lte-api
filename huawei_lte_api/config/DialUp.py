from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class DialUp(ApiGroup):
    def config(self) -> GetResponseType:
        return self._session.get('dialup/config.xml', prefix='config')

    def connectmode(self) -> GetResponseType:
        return self._session.get('dialup/connectmode.xml', prefix='config')

    def profileswitch(self) -> GetResponseType:
        return self._session.get('dialup/profileswitch.xml', prefix='config')

    def lmt_auto_mode_disconnect(self) -> GetResponseType:
        return self._session.get('dialup/lmt_auto_mode_disconnect.xml', prefix='config')
