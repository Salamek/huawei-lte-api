from huawei_lte_api.ApiGroup import ApiGroup


class SNtp(ApiGroup):
    def get_settings(self) -> dict:
        return self._connection.get('sntp/settings')

    def sntpswitch(self) -> dict:
        return self._connection.get('sntp/sntpswitch')

    def serverinfo(self) -> dict:
        return self._connection.get('sntp/serverinfo')

    def timeinfo(self) -> dict:
        return self._connection.get('sntp/timeinfo')
