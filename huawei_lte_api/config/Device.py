from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class Device(ApiGroup):
    def config(self) -> GetResponseType:
        return self._connection.get('device/config.xml', prefix='config')
