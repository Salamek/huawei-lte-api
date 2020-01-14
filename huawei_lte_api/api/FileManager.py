import os
from typing import BinaryIO
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import SetResponseType


class FileManager(ApiGroup):
    def upload(self, uploadfile: BinaryIO, uploadfile_name: str) -> SetResponseType:
        """
        Uploads firmware update and triggers it
        :param uploadfile: filehandle on file to upload
        :param uploadfile_name: name of uploaded file
        :return: str
        """
        uploadfile_basename = os.path.basename(uploadfile_name)
        _, extension = os.path.splitext(uploadfile_basename)

        if extension.lower() not in ['.bin', '.zip']:
            raise Exception('Only *.bin or *.zip is allowed')

        return self._connection.post_file('filemanager/upload', {
            'uploadfile': uploadfile,
        }, {
            'cur_path': 'OU:{}'.format(uploadfile_basename)
        })
