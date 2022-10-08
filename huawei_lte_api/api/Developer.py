from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Developer(ApiGroup):
    def developermode_featureswitch(self) -> GetResponseType:
        return self._session.get('developer/developermode-featureswitch')

    def atport_status(self) -> GetResponseType:
        return self._session.get('app/atport-status')
