
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class Global(ApiGroup):
    def module_switch(self):
        return self._connection.get('global/module-switch')
