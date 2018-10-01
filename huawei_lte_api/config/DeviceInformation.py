from huawei_lte_api.ApiGroup import ApiGroup


class DeviceInformation(ApiGroup):
    def config(self):
        return self._connection.get(
            'deviceinformation/config.xml', prefix='config')
