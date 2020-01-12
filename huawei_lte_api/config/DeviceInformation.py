from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class DeviceInformation(ApiGroup):
    def config(self) -> GetResponseType:
        return self._connection.get(
            'deviceinformation/config.xml', prefix='config')
