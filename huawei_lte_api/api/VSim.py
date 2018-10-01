
from huawei_lte_api.ApiGroup import ApiGroup


class VSim(ApiGroup):
    def operateswitch_vsim(self) -> dict:
        return self._connection.get('vsim/operateswitch-vsim')
