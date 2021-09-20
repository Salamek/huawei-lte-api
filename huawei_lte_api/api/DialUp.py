from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType, SetResponseType


class DialUp(ApiGroup):
    def mobile_dataswitch(self) -> GetResponseType:
        """
        Get current LTE modem toggle state
        :return:
        """
        return self._session.get('dialup/mobile-dataswitch')

    def connection(self) -> GetResponseType:
        return self._session.get('dialup/connection')

    def dialup_feature_switch(self) -> GetResponseType:
        return self._session.get('dialup/dialup-feature-switch')

    def profiles(self) -> GetResponseType:
        return self._session.get('dialup/profiles')

    def auto_apn(self) -> GetResponseType:
        return self._session.get('dialup/auto-apn')

    def dial(self) -> SetResponseType:
        return self._session.post_set('dialup/dial', {
            'Action': 1
        })

    def set_mobile_dataswitch(self, dataswitch: int = 0) -> SetResponseType:
        """
        Toggle LTE modem state
        :param dataswitch: 0 to disable LTE modem, 1 to enable LTE modem
        """
        return self._session.post_set('dialup/mobile-dataswitch', {
            'dataswitch': dataswitch
        })
