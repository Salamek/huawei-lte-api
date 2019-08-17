from huawei_lte_api.ApiGroup import ApiGroup


class Pincode(ApiGroup):
    def config(self):
        return self._connection.get('pincode/config.xml', prefix='config')
