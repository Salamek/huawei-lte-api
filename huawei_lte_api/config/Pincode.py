from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class Pincode(ApiGroup):
    def config(self) -> GetResponseType:
        return self._connection.get('pincode/config.xml', prefix='config')
