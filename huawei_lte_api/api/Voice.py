from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class Voice(ApiGroup):
    def featureswitch(self) -> dict:
        return self._connection.get('voice/featureswitch')

    @authorized_call
    def sipaccount(self) -> dict:
        return self._connection.get('voice/sipaccount')

    @authorized_call
    def sipadvance(self) -> dict:
        return self._connection.get('voice/sipadvance')

    @authorized_call
    def sipserver(self) -> dict:
        return self._connection.get('voice/sipserver')

    @authorized_call
    def speeddial(self) -> dict:
        return self._connection.get('voice/speeddial')
