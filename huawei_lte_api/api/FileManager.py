
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class FileManager(ApiGroup):
    def upload(self, uploadfile: str):
        return self._connection.post('filemanager/upload', {
            'uploadfile': uploadfile
        })  # !FIXME