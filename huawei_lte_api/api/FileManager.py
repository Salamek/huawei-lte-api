from pathlib import Path
from typing import BinaryIO

from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import SetResponseType


class FileManager(ApiGroup):
    def upload(self, uploadfile: BinaryIO, uploadfile_name: str) -> SetResponseType:
        """
        Uploads firmware update and triggers it
        :param uploadfile: filehandle on file to upload
        :param uploadfile_name: name of uploaded file
        :return: str
        """

        uploadfile_name_path = Path(uploadfile_name)

        if uploadfile_name_path.suffix.lower() not in [".bin", ".zip"]:
            msg = "Only *.bin or *.zip is allowed"
            raise ValueError(msg)

        return self._session.post_file("filemanager/upload", {
            "uploadfile": uploadfile,
        }, {
            "cur_path": f"OU:{uploadfile_name_path.name}",
        })
