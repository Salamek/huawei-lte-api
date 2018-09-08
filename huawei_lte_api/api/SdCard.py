from huawei_lte_api.ApiGroup import ApiGroup


class SdCard(ApiGroup):

    def dlna_setting(self) -> dict:
        return self._connection.get('sdcard/dlna-setting')

    def sdcard(self) -> dict:
        return self._connection.get('sdcard/sdcard')
