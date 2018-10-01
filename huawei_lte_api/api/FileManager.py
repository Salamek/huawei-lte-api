
from huawei_lte_api.ApiGroup import ApiGroup


class FileManager(ApiGroup):
    def upload(self, uploadfile: str):
        return self._connection.post('filemanager/upload', {
            'uploadfile': uploadfile
        })  # !FIXME see issue #2
