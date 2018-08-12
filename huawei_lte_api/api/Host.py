import datetime
from huawei_lte_api.ApiGroup import ApiGroup


class Host(ApiGroup):
    def info(self, datetime: datetime.datetime, platform: str, useragent: str, version: str):
        return self._connection.post('host/info', {
            'Time': datetime.strftime('%Y%m%d%H%M%S'),
            'Timezone': 'GMT{}'.format(datetime.strftime('%z')),
            'Platform': platform,
            'PlatformVer': useragent,
            'Navigator': version,
            'NavigatorVer': useragent
        })