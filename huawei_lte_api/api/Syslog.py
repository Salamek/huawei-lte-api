from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType, SetResponseType


class Syslog(ApiGroup):
    def querylog(self) -> GetResponseType:
        return self._connection.get('syslog/querylog')

    def clear(self) -> SetResponseType:
        return self._connection.post_set('syslog/processlog', {
            'command': 'clear',
        })
