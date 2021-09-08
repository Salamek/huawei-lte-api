from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Global(ApiGroup):
    def languagelist(self) -> GetResponseType:
        return self._session.get('global/languagelist.xml', prefix='config')

    def config(self) -> GetResponseType:
        return self._session.get('global/config.xml', prefix='config')

    def net_type(self) -> GetResponseType:
        return self._session.get('global/net-type.xml', prefix='config')
