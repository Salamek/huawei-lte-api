from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Ussd(ApiGroup):
    def prepaidussd(self) -> GetResponseType:
        return self._session.get('ussd/prepaidussd.xml', prefix='config')

    def postpaidussd(self) -> GetResponseType:
        return self._session.get('ussd/postpaidussd.xml', prefix='config')
