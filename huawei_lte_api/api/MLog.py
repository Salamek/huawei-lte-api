from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class MLog(ApiGroup):
    def mobile_logger(self) -> GetResponseType:
        """
        Get mobile logger information.

        Endpoint found by reverse engineering B310s-22 firmware, unknown usage.

        :return: Mobile logger information.

        Usage example:
        >>> mlog = MLog(session)
        >>> mobile_logger_info = mlog.mobile_logger()
        >>> print(mobile_logger_info)
        """
        return self._session.get("mlog/mobile-logger")
