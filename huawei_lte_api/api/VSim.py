
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class VSim(ApiGroup):
    def operateswitch_vsim(self) -> dict:
        return self._connection.get('vsim/operateswitch-vsim')
