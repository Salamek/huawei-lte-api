from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Sms(ApiGroup):
    def config(self) -> GetResponseType:
        return self._session.get('sms/config.xml', prefix='config')
