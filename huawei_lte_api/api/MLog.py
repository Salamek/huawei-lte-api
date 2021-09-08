from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class MLog(ApiGroup):
    def mobile_logger(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._session.get('mlog/mobile-logger')
