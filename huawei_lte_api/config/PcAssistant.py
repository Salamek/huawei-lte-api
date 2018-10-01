
from huawei_lte_api.ApiGroup import ApiGroup


class PcAssistant(ApiGroup):
    def config(self):
        return self._connection.get('pcassistant/config.xml', prefix='config')
