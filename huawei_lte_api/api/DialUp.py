
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class DialUp(ApiGroup):
    def mobile_dataswitch(self) ->dict:
        return self._connection.get('dialup/mobile-dataswitch')

    def connection(self) ->dict:
        return self._connection.get('dialup/connection')

    def dialup_feature_switch(self) ->dict:
        return self._connection.get('dialup/dialup-feature-switch')

    @authorized_call
    def profiles(self) ->dict:
        return self._connection.get('dialup/profiles')

    def auto_apn(self) ->dict:
        return self._connection.get('dialup/auto-apn')

    def dial(self):
        return self._connection.post('dialup/dial', {
            'Action': 1
        })

    def set_mobile_dataswitch(self, dataswitch: int=0):
        return self._connection.post('dialup/mobile-dataswitch', {
            'dataswitch': dataswitch
        })