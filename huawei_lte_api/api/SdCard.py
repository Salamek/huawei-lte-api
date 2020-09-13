from collections import OrderedDict
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType, SetResponseType


class SdCard(ApiGroup):

    def dlna_setting(self) -> GetResponseType:
        return self._connection.get('sdcard/dlna-setting')

    def set_dlna_setting(self, enabled: bool, share_all: bool,
                         share_path: str = '/') -> SetResponseType:
        return self._connection.post_set('sdcard/dlna-setting', {
            'enabled': int(enabled),
            'sharepath': share_path,
            'shareallpath': int(share_all),
        })

    def sdcard(self) -> GetResponseType:
        return self._connection.get('sdcard/sdcard')

    def sdcardsamba(self) -> GetResponseType:
        return self._connection.get('sdcard/sdcardsamba')

    def set_sdcardsamba(self, enabled: bool,
                        server_name: str = 'homerouter.cpe',
                        server_description: str = 'samba server',
                        workgroup_name: str = 'WORKGROUP',
                        anonymous_access: bool = False,
                        printer_enabled: bool = True) -> SetResponseType:
        return self._connection.post_set('sdcard/sdcardsamba', OrderedDict((
            ('enabled', int(enabled)),
            ('servername', server_name),
            ('serverdescription', server_description),
            ('workgroupname', workgroup_name),
            ('anonymousaccess', int(anonymous_access)),
            ('printerenable', int(printer_enabled)),
        )))

    def printerlist(self) -> GetResponseType:
        return self._connection.get('sdcard/printerlist')

    def share_account(self) -> GetResponseType:
        return self._connection.get('sdcard/share-account')

    def sdfile(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._connection.get('sdcard/sdfile')

    def fileupload(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._connection.get('sdcard/fileupload')

    def check_file_exist(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._connection.get('sdcard/Check_file_exist')

    def createdir(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._connection.get('sdcard/createdir')

    def deletefile(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._connection.get('sdcard/deletefile')
