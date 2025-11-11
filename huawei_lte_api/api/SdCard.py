from __future__ import annotations

import datetime
from collections import OrderedDict
from typing import TYPE_CHECKING

from huawei_lte_api.ApiGroup import ApiGroup

if TYPE_CHECKING:
    from huawei_lte_api.Session import GetResponseType, SetResponseType


class SdCard(ApiGroup):

    def dlna_setting(self) -> GetResponseType:
        return self._session.get("sdcard/dlna-setting")

    def set_dlna_setting(self, enabled: bool, share_all: bool,
                         share_path: str = "/") -> SetResponseType:
        """
        Sets DLNA settings
        :param enabled: is DLNA enabled
        :param share_all: Share all
        :param share_path: What path to share defaults to /
        :return:
        """
        return self._session.post_set("sdcard/dlna-setting", {
            "enabled": int(enabled),
            "sharepath": share_path,
            "shareallpath": int(share_all),
        })

    def sdcard(self) -> GetResponseType:
        """
        Get information about sharing
        :return:
        """
        return self._session.get("sdcard/sdcard")

    def sdcardsamba(self) -> GetResponseType:
        return self._session.get("sdcard/sdcardsamba")

    def set_sdcardsamba(self, enabled: bool,
                        server_name: str = "homerouter.cpe",
                        server_description: str = "samba server",
                        workgroup_name: str = "WORKGROUP",
                        anonymous_access: bool = False,
                        printer_enabled: bool = True) -> SetResponseType:
        """
        Enable file sharing using SMB
        :return:
        :param enabled: is enabled
        :param server_name: Name of the server on your W/LAN
        :param server_description: Description of SMB server
        :param workgroup_name: Workgroup name
        :param anonymous_access: enable anonymous access
        :param printer_enabled: enable printer
        :return:
        """
        return self._session.post_set("sdcard/sdcardsamba", OrderedDict((
            ("enabled", int(enabled)),
            ("servername", server_name),
            ("serverdescription", server_description),
            ("workgroupname", workgroup_name),
            ("anonymousaccess", int(anonymous_access)),
            ("printerenable", int(printer_enabled)),
        )))

    def printerlist(self) -> GetResponseType:
        return self._session.get("sdcard/printerlist")

    def share_account(self) -> GetResponseType:
        """???
        <request>
        <accounts>
            <account>
                <accountname></accountname>
                <accountpwd></accountpwd>
                <sharepath></sharepath>
                <accesstype></accesstype>
                <shareallpath></shareallpath>
            </account>
            <account>
                ...
            </account>
            ...
        </accounts>
    </request>
        :return:
        """
        return self._session.get("sdcard/share-account")

    def sdfile(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._session.get("sdcard/sdfile")

    def fileupload(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._session.get("sdcard/fileupload")

    def check_file_exist(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._session.get("sdcard/Check_file_exist")

    def create_dir(self, name: str, current_path: str = "/", created: datetime.datetime | None = None) -> SetResponseType:
        """
        Create directory on the SD card
        :param name: Name of dir to create
        :param current_path: In what path to create, default is /
        :param created: datetime of creation
        :return: ResponseEnum.OK on success
        """

        if not created:
            created = datetime.datetime.now()

        return self._session.post_set("sdcard/createdir", {
            "CurrentPath": current_path,
            "FileName": name,
            "Time": {
                "Year": created.year,
                "Month": created.month,
                "Day": created.day,
                "Hour": created.hour,
                "Min": created.minute,
                "Sec": created.second,
            },
        })

    def delete_file(self, name: str, current_path: str = "/") -> SetResponseType:
        """
        Delete file or directory on SD card
        :param name: name to delete
        :param current_path: in what path to delete
        :return: ResponseEnum.OK on success
        """
        return self._session.post_set("sdcard/deletefile", {
            "CurrentPath": current_path,
            "DeleteFileList": name,
        })

    def sd_capacity(self) -> GetResponseType:
        """
        Gets information about SD-card capacity
        :return:
        """
        return self._session.get("sdcard/sdcapacity")
