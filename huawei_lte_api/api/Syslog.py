from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType, SetResponseType


class Syslog(ApiGroup):
    def querylog(self) -> GetResponseType:
        return self._session.get('syslog/querylog')

    def clear(self) -> SetResponseType:
        return self._session.post_set('syslog/processlog', {
            'command': 'clear',
        })
