from huawei_lte_api.ApiGroup import ApiGroup


class Syslog(ApiGroup):
    def querylog(self) -> dict:
        return self._connection.get('syslog/querylog')

    def clear(self):
        return self._connection.post('syslog/processlog', {
            'command': 'clear',
        })
