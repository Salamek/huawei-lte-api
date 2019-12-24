from huawei_lte_api.ApiGroup import ApiGroup, GetResponseType


class VSim(ApiGroup):
    def operateswitch_vsim(self) -> GetResponseType:
        return self._connection.get('vsim/operateswitch-vsim')
