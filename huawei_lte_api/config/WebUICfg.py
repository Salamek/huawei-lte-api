from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class WebUICfg(ApiGroup):
    def config(self):
        return self._connection.get('webuicfg/config.xml', prefix='config')
