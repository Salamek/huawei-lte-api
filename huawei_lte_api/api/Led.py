from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Led(ApiGroup):
    def nightmode(self) -> GetResponseType:
        return self._session.get('led/nightmode')

    def appctrlled(self) -> GetResponseType:
        return self._session.get('led/appctrlled')
