
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class DDns(ApiGroup):
    @authorized_call
    def get_ddns_list(self) -> dict:
        return self._connection.get('ddns/ddns-list')

    def get_status(self) ->dict:
        return self._connection.get('ddns/status')