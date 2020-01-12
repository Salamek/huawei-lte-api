from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class Sms(ApiGroup):
    def config(self) -> GetResponseType:
        return self._connection.get('sms/config.xml', prefix='config')
