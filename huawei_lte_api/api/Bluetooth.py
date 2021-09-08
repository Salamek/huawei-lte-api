from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Bluetooth(ApiGroup):
    def settings(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._session.get('bluetooth/settings')

    def scan(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._session.get('bluetooth/scan')
