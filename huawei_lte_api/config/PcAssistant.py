from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class PcAssistant(ApiGroup):
    def config(self) -> GetResponseType:
        return self._session.get('pcassistant/config.xml', prefix='config')

    def updateautorun(self) -> GetResponseType:
        return self._session.get('pcassistant/updateautorun.xml', prefix='config')
