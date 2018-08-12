
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class Security(ApiGroup):

    def bridgemode(self):
        return self._connection.get('security/bridgemode')