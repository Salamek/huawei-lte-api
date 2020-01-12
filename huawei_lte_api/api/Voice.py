from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class Voice(ApiGroup):
    def featureswitch(self) -> GetResponseType:
        return self._connection.get('voice/featureswitch')

    def sipaccount(self) -> GetResponseType:
        return self._connection.get('voice/sipaccount')

    def sipadvance(self) -> GetResponseType:
        return self._connection.get('voice/sipadvance')

    def sipserver(self) -> GetResponseType:
        return self._connection.get('voice/sipserver')

    def speeddial(self) -> GetResponseType:
        return self._connection.get('voice/speeddial')

    def functioncode(self) -> GetResponseType:
        return self._connection.get('voice/functioncode')

    def voiceadvance(self) -> GetResponseType:
        return self._connection.get('voice/voiceadvance')
