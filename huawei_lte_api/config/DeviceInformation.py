from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class DeviceInformation(ApiGroup):
    def config(self):
        return self._connection.get(
            'deviceinformation/config.xml', prefix='config')
