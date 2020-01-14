from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class PcAssistant(ApiGroup):
    def config(self) -> GetResponseType:
        return self._connection.get('pcassistant/config.xml', prefix='config')

    def updateautorun(self) -> GetResponseType:
        return self._connection.get('pcassistant/updateautorun.xml', prefix='config')
