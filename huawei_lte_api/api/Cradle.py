

from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class Cradle(ApiGroup):
    def status_info(self):
        return self.connection.get('cradle/status-info')
