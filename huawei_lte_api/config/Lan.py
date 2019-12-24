from huawei_lte_api.ApiGroup import ApiGroup, GetResponseType


class Lan(ApiGroup):
    def config(self) -> GetResponseType:
        return self._connection.get('lan/config.xml', prefix='config')
