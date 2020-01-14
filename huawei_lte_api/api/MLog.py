from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class MLog(ApiGroup):
    def mobile_logger(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._connection.get('mlog/mobile-logger')
