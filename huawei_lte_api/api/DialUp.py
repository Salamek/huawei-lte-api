
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class DialUp(ApiGroup):
    def mobile_dataswitch(self):
        return self._connection.get('dialup/mobile-dataswitch')

    def connection(self):
        return self._connection.get('dialup/connection')

    def dial(self):
        return self._connection.post('dialup/dial', {
            'Action': 1
        })

    def set_mobile_dataswitch(self, dataswitch: int=0):
        return self._connection.post('dialup/mobile-dataswitch', {
            'dataswitch': dataswitch
        })