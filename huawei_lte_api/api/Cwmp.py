from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Cwmp(ApiGroup):
    def basic_info(self) -> GetResponseType:
        return self._session.get('cwmp/basic-info')
