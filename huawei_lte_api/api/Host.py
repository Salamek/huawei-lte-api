import datetime
from collections import OrderedDict
from huawei_lte_api.ApiGroup import ApiGroup


class Host(ApiGroup):
    def info(self, date_time: datetime.datetime, platform: str, user_agent: str, version: str):
        return self._connection.post('host/info', OrderedDict((
            ('Time', date_time.strftime('%Y%m%d%H%M%S')),
            ('Timezone', 'GMT{}'.format(date_time.strftime('%z'))),
            ('Platform', platform),
            ('PlatformVer', user_agent),
            ('Navigator', version),
            ('NavigatorVer', user_agent)
        )))
