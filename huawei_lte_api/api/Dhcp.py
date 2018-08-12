
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class Dhcp(ApiGroup):
    def settings(self) -> dict:
        return self._connection.get('dhcp/settings')
