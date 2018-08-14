
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class Monitoring(ApiGroup):
    def converged_status(self) -> dict:
        return self._connection.get('monitoring/converged-status')

    def status(self) -> dict:
        return self._connection.get('monitoring/status')

    def check_notifications(self) -> dict:
        return self._connection.get('monitoring/check-notifications')

    def traffic_statistics(self) -> dict:
        return self._connection.get('monitoring/traffic-statistics')

    def start_date(self) -> dict:
        return self._connection.get('monitoring/start_date')

    def set_start_date(self, start_day: int, data_limit: str, month_threshold: int):
        """
        Sets network usage alarm for LTE
        :param start_day: number of day when monitoring starts
        :param data_limit: Maximal data limit as string eg.: 1000MB or 1GB and so on
        :param month_threshold: Alarm threshold in % as int number eg.: 90
        :return: dict
        """
        return self._connection.post('monitoring/start_date', {
            'StartDay': start_day,
            'DataLimit': data_limit,
            'MonthThreshold': month_threshold,
            'SetMonthData': 1
        })

    def start_date_wlan(self) -> dict:
        return self._connection.get('monitoring/start_date_wlan')

    def set_start_date_wlan(self, start_day: int, data_limit: str, month_threshold: int):
        """
        Sets network usage alarm for WLAN
        :param start_day: number of day when monitoring starts
        :param data_limit: Maximal data limit as string eg.: 1000MB or 1GB and so on
        :param month_threshold: Alarm threshold in % as int number eg.: 90
        :return: dict
        """
        return self._connection.post('monitoring/start_date_wlan', {
            'StartDay': start_day,
            'DataLimit': data_limit,
            'MonthThreshold': month_threshold,
            'SettingEnable': 1  #!FIXME
        })

    def month_statistics(self) -> dict:
        return self._connection.get('monitoring/month_statistics')

    def month_statistics_wlan(self) -> dict:
        return self._connection.get('monitoring/month_statistics_wlan')

    def set_clear_traffic(self) -> dict:
        return self._connection.post('monitoring/clear-traffic', {
            'ClearTraffic': 1
        })