from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class Global(ApiGroup):
    def languagelist(self) -> GetResponseType:
        return self._connection.get('global/languagelist.xml', prefix='config')

    def config(self) -> GetResponseType:
        return self._connection.get('global/config.xml', prefix='config')

    def net_type(self) -> GetResponseType:
        return self._connection.get('global/net-type.xml', prefix='config')
