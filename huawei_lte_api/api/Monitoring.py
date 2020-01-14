from collections import OrderedDict
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType, SetResponseType


class Monitoring(ApiGroup):
    def converged_status(self) -> GetResponseType:
        return self._connection.get('monitoring/converged-status')

    def status(self) -> GetResponseType:
        return self._connection.get('monitoring/status')

    def check_notifications(self) -> GetResponseType:
        return self._connection.get('monitoring/check-notifications')

    def traffic_statistics(self) -> GetResponseType:
        return self._connection.get('monitoring/traffic-statistics')

    def start_date(self) -> GetResponseType:
        return self._connection.get('monitoring/start_date')

    def set_start_date(self, start_day: int, data_limit: str, month_threshold: int) -> SetResponseType:
        """
        Sets network usage alarm for LTE
        :param start_day: number of day when monitoring starts
        :param data_limit: Maximal data limit as string eg.: 1000MB or 1GB and so on
        :param month_threshold: Alarm threshold in % as int number eg.: 90
        :return: dict
        """
        return self._connection.post_set('monitoring/start_date', OrderedDict((
            ('StartDay', start_day),
            ('DataLimit', data_limit),
            ('MonthThreshold', month_threshold),
            ('SetMonthData', 1)
        )))

    def start_date_wlan(self) -> GetResponseType:
        return self._connection.get('monitoring/start_date_wlan')

    def set_start_date_wlan(self, start_day: int, data_limit: str, month_threshold: int) -> SetResponseType:
        """
        Sets network usage alarm for WLAN
        :param start_day: number of day when monitoring starts
        :param data_limit: Maximal data limit as string eg.: 1000MB or 1GB and so on
        :param month_threshold: Alarm threshold in % as int number eg.: 90
        :return: dict
        """
        return self._connection.post_set('monitoring/start_date_wlan', OrderedDict((
            ('StartDay', start_day),
            ('DataLimit', data_limit),
            ('MonthThreshold', month_threshold),
            ('SettingEnable', 1)  #!FIXME
        )))

    def month_statistics(self) -> GetResponseType:
        return self._connection.get('monitoring/month_statistics')

    def month_statistics_wlan(self) -> GetResponseType:
        return self._connection.get('monitoring/month_statistics_wlan')

    def set_clear_traffic(self) -> SetResponseType:
        return self._connection.post_set('monitoring/clear-traffic', {
            'ClearTraffic': 1
        })

    def wifi_month_setting(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage, probably not implemented by Huawei
        :return:
        """
        return self._connection.get('monitoring/wifi-month-setting')
