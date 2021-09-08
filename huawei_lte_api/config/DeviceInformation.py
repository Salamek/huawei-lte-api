from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class DeviceInformation(ApiGroup):
    def config(self) -> GetResponseType:
        return self._session.get(
            'deviceinformation/config.xml', prefix='config')
