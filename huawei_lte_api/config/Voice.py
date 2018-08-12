
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class Voice(ApiGroup):
    def config(self):
        return self._connection.get('voice/config.xml', prefix='config')