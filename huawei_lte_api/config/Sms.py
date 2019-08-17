from huawei_lte_api.ApiGroup import ApiGroup


class Sms(ApiGroup):
    def config(self):
        return self._connection.get('sms/config.xml', prefix='config')
