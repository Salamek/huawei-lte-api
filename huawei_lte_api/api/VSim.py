from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class VSim(ApiGroup):
    def operateswitch_vsim(self) -> GetResponseType:
        return self._session.get('vsim/operateswitch-vsim')
