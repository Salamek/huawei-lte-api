from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class SNtp(ApiGroup):
    def get_settings(self) -> GetResponseType:
        return self._session.get('sntp/settings')

    def sntpswitch(self) -> GetResponseType:
        return self._session.get('sntp/sntpswitch')

    def serverinfo(self) -> GetResponseType:
        return self._session.get('sntp/serverinfo')

    def timeinfo(self) -> GetResponseType:
        return self._session.get('sntp/timeinfo')
