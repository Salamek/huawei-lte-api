from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class SNtp(ApiGroup):
    def get_settings(self) -> GetResponseType:
        return self._connection.get('sntp/settings')

    def sntpswitch(self) -> GetResponseType:
        return self._connection.get('sntp/sntpswitch')

    def serverinfo(self) -> GetResponseType:
        return self._connection.get('sntp/serverinfo')

    def timeinfo(self) -> GetResponseType:
        return self._connection.get('sntp/timeinfo')
