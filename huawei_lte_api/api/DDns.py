from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class DDns(ApiGroup):
    def get_ddns_list(self) -> GetResponseType:
        return self._session.get('ddns/ddns-list')

    def get_status(self) -> GetResponseType:
        return self._session.get('ddns/status')

    def serverlist(self) -> GetResponseType:
        return self._session.get('ddns/serverlist')
