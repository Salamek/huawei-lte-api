import datetime
from collections import OrderedDict

from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import SetResponseType


class Host(ApiGroup):
    def info(self, date_time: datetime.datetime, platform: str, user_agent: str, version: str) -> SetResponseType:
        """
        Send host information to the server.

        :param date_time: Current date and time.
        :param platform: Platform information.
        :param user_agent: User agent string.
        :param version: Version information.
        :return: Set response type.

        Usage example:
        >>> host = Host(session)
        >>> response = host.info(datetime.datetime.now(), "Windows", "Mozilla/5.0", "1.0")
        >>> print(response)
        """
        return self._session.post_set('host/info', OrderedDict((
            ('Time', date_time.strftime('%Y%m%d%H%M%S')),
            ('Timezone', 'GMT{}'.format(date_time.strftime('%z'))),
            ('Platform', platform),
            ('PlatformVer', user_agent),
            ('Navigator', version),
            ('NavigatorVer', user_agent)
        )))
