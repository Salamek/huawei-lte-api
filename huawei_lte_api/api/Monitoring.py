from collections import OrderedDict

from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType, SetResponseType


class Monitoring(ApiGroup):
    def converged_status(self) -> GetResponseType:
        """
        Get the converged status of the router.

        :return: Converged status.

        Usage example:
        >>> monitoring = Monitoring(session)
        >>> converged_status = monitoring.converged_status()
        >>> print(converged_status)
        """
        return self._session.get('monitoring/converged-status')

    def status(self) -> GetResponseType:
        """
        Returns status info of the router.
        Note: for signal some routers return correct value in SignalIcon some in SignalIconNr.

        :return: Status info of the router.

        Usage example:
        >>> monitoring = Monitoring(session)
        >>> status_info = monitoring.status()
        >>> print(status_info)
        """
        return self._session.get('monitoring/status')

    def check_notifications(self) -> GetResponseType:
        """
        Check for notifications.

        :return: Notifications.

        Usage example:
        >>> monitoring = Monitoring(session)
        >>> notifications = monitoring.check_notifications()
        >>> print(notifications)
        """
        return self._session.get('monitoring/check-notifications')

    def traffic_statistics(self) -> GetResponseType:
        """
        Get traffic statistics.

        :return: Traffic statistics.

        Usage example:
        >>> monitoring = Monitoring(session)
        >>> traffic_stats = monitoring.traffic_statistics()
        >>> print(traffic_stats)
        """
        return self._session.get('monitoring/traffic-statistics')

    def start_date(self) -> GetResponseType:
        """
        Get the start date for monitoring.

        :return: Start date.

        Usage example:
        >>> monitoring = Monitoring(session)
        >>> start_date = monitoring.start_date()
        >>> print(start_date)
        """
        return self._session.get('monitoring/start_date')

    def set_start_date(self, start_day: int, data_limit: str, month_threshold: int) -> SetResponseType:
        """
        Sets network usage alarm for LTE.

        :param start_day: Number of day when monitoring starts.
        :param data_limit: Maximal data limit as string eg.: 1000MB or 1GB and so on.
        :param month_threshold: Alarm threshold in % as int number eg.: 90.
        :return: Set response type.

        Usage example:
        >>> monitoring = Monitoring(session)
        >>> response = monitoring.set_start_date(start_day=1, data_limit="1GB", month_threshold=90)
        >>> print(response)
        """
        return self._session.post_set('monitoring/start_date', OrderedDict((
            ('StartDay', start_day),
            ('DataLimit', data_limit),
            ('MonthThreshold', month_threshold),
            ('SetMonthData', 1)
        )))

    def start_date_wlan(self) -> GetResponseType:
        """
        Get the start date for WLAN monitoring.

        :return: Start date for WLAN monitoring.

        Usage example:
        >>> monitoring = Monitoring(session)
        >>> start_date_wlan = monitoring.start_date_wlan()
        >>> print(start_date_wlan)
        """
        return self._session.get('monitoring/start_date_wlan')

    def set_start_date_wlan(self, start_day: int, data_limit: str, month_threshold: int) -> SetResponseType:
        """
        Sets network usage alarm for WLAN.

        :param start_day: Number of day when monitoring starts.
        :param data_limit: Maximal data limit as string eg.: 1000MB or 1GB and so on.
        :param month_threshold: Alarm threshold in % as int number eg.: 90.
        :return: Set response type.

        Usage example:
        >>> monitoring = Monitoring(session)
        >>> response = monitoring.set_start_date_wlan(start_day=1, data_limit="1GB", month_threshold=90)
        >>> print(response)
        """
        return self._session.post_set('monitoring/start_date_wlan', OrderedDict((
            ('StartDay', start_day),
            ('DataLimit', data_limit),
            ('MonthThreshold', month_threshold),
            ('SettingEnable', 1)  # !FIXME
        )))

    def month_statistics(self) -> GetResponseType:
        """
        Get monthly statistics.

        :return: Monthly statistics.

        Usage example:
        >>> monitoring = Monitoring(session)
        >>> month_stats = monitoring.month_statistics()
        >>> print(month_stats)
        """
        return self._session.get('monitoring/month_statistics')

    def month_statistics_wlan(self) -> GetResponseType:
        """
        Get monthly statistics for WLAN.

        :return: Monthly statistics for WLAN.

        Usage example:
        >>> monitoring = Monitoring(session)
        >>> month_stats_wlan = monitoring.month_statistics_wlan()
        >>> print(month_stats_wlan)
        """
        return self._session.get('monitoring/month_statistics_wlan')

    def set_clear_traffic(self) -> SetResponseType:
        """
        Clear traffic statistics.

        :return: Set response type.

        Usage example:
        >>> monitoring = Monitoring(session)
        >>> response = monitoring.set_clear_traffic()
        >>> print(response)
        """
        return self._session.post_set('monitoring/clear-traffic', {
            'ClearTraffic': 1
        })

    def wifi_month_setting(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage, probably not implemented by Huawei.

        :return: WiFi month setting.

        Usage example:
        >>> monitoring = Monitoring(session)
        >>> wifi_month_setting = monitoring.wifi_month_setting()
        >>> print(wifi_month_setting)
        """
        return self._session.get('monitoring/wifi-month-setting')

    def daily_data_limit(self) -> GetResponseType:
        """
        Get daily data limit.

        :return: Daily data limit.

        Usage example:
        >>> monitoring = Monitoring(session)
        >>> daily_data_limit = monitoring.daily_data_limit()
        >>> print(daily_data_limit)
        """
        return self._session.get('monitoring/daily-data-limit')

    def statistic_feature_switch(self) -> GetResponseType:
        """
        Get the status of the statistic feature switch.

        :return: Statistic feature switch status.

        Usage example:
        >>> monitoring = Monitoring(session)
        >>> statistic_feature_switch = monitoring.statistic_feature_switch()
        >>> print(statistic_feature_switch)
        """
        return self._session.get('monitoring/statistic-feature-switch')
