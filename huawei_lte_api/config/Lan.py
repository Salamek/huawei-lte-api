from huawei_lte_api.ApiGroup import ApiGroup


class Lan(ApiGroup):
    def config(self):
        return self._connection.get('lan/config.xml', prefix='config')
