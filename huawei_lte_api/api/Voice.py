from huawei_lte_api.ApiGroup import ApiGroup


class Voice(ApiGroup):
    def featureswitch(self) -> dict:
        return self._connection.get('voice/featureswitch')

    def sipaccount(self) -> dict:
        return self._connection.get('voice/sipaccount')

    def sipadvance(self) -> dict:
        return self._connection.get('voice/sipadvance')

    def sipserver(self) -> dict:
        return self._connection.get('voice/sipserver')

    def speeddial(self) -> dict:
        return self._connection.get('voice/speeddial')

    def functioncode(self) -> dict:
        return self._connection.get('voice/functioncode')

    def voiceadvance(self) -> dict:
        return self._connection.get('voice/voiceadvance')
