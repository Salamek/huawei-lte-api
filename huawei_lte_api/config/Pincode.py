from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Pincode(ApiGroup):
    def config(self) -> GetResponseType:
        return self._session.get('pincode/config.xml', prefix='config')
