
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class Global(ApiGroup):
    def languagelist(self):
        return self._connection.get('global/languagelist.xml', prefix='config')

    def config(self):
        return self._connection.get('global/config.xml', prefix='config')

    def net_type(self):
        return self._connection.get('global/net-type.xml', prefix='config')