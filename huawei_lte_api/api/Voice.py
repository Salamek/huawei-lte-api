from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Voice(ApiGroup):
    def featureswitch(self) -> GetResponseType:
        return self._session.get('voice/featureswitch')

    def sipaccount(self) -> GetResponseType:
        return self._session.get('voice/sipaccount')

    def sipadvance(self) -> GetResponseType:
        return self._session.get('voice/sipadvance')

    def sipserver(self) -> GetResponseType:
        return self._session.get('voice/sipserver')

    def speeddial(self) -> GetResponseType:
        return self._session.get('voice/speeddial')

    def functioncode(self) -> GetResponseType:
        return self._session.get('voice/functioncode')

    def voiceadvance(self) -> GetResponseType:
        return self._session.get('voice/voiceadvance')

    def voicebusy(self) -> GetResponseType:
        return self._session.get('voice/voicebusy')

    def codec(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage, probably not implemented by Huawei
        :return:
        """
        return self._session.get('voice/codec')
