from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class WebUICfg(ApiGroup):
    def config(self) -> GetResponseType:
        return self._connection.get('webuicfg/config.xml', prefix='config')
