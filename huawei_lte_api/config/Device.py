from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Device(ApiGroup):
    def config(self) -> GetResponseType:
        return self._session.get('device/config.xml', prefix='config')
