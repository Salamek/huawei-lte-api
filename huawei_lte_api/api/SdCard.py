from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class SdCard(ApiGroup):

    def dlna_setting(self) -> dict:
        return self._connection.get('sdcard/dlna-setting')

    def sdcard(self) -> dict:
        return self._connection.get('sdcard/sdcard')

    def sdcardsamba(self) -> dict:
        return self._connection.get('sdcard/sdcardsamba')

    def printerlist(self) -> dict:
        return self._connection.get('sdcard/printerlist')

    @authorized_call
    def share_account(self) -> dict:
        return self._connection.get('sdcard/share-account')
