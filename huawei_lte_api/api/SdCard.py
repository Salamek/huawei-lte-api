from collections import OrderedDict
from huawei_lte_api.ApiGroup import ApiGroup


class SdCard(ApiGroup):

    def dlna_setting(self) -> dict:
        return self._connection.get('sdcard/dlna-setting')

    def set_dlna_setting(self, enabled: bool, share_all: bool,
                         share_path: str = '/'):
        return self._connection.post('sdcard/dlna-setting', {
            'enabled': int(enabled),
            'sharepath': share_path,
            'shareallpath': int(share_all),
        })

    def sdcard(self) -> dict:
        return self._connection.get('sdcard/sdcard')

    def sdcardsamba(self) -> dict:
        return self._connection.get('sdcard/sdcardsamba')

    def set_sdcardsamba(self, enabled: bool,
                        server_name: str = 'homerouter.cpe',
                        server_description: str = 'samba server',
                        workgroup_name: str = 'WORKGROUP',
                        anonymous_access: bool = False,
                        printer_enabled: bool = True):
        return self._connection.post('sdcard/sdcardsamba', OrderedDict((
            ('enabled', int(enabled)),
            ('servername', server_name),
            ('serverdescription', server_description),
            ('workgroupname', workgroup_name),
            ('anonymousaccess', int(anonymous_access)),
            ('printerenable', int(printer_enabled)),
        )))

    def printerlist(self) -> dict:
        return self._connection.get('sdcard/printerlist')

    def share_account(self) -> dict:
        return self._connection.get('sdcard/share-account')
