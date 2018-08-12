
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class PcAssistant(ApiGroup):
    def config(self):
        return self._connection.get('pcassistant/config.xml', prefix='config')