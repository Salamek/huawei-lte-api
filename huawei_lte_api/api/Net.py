
from huawei_lte_api.ApiGroup import ApiGroup


class Net(ApiGroup):
    def current_plmn(self):
        return self._connection.get('net/current-plmn')