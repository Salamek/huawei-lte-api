from huawei_lte_api.ApiGroup import ApiGroup, GetResponseType


class DDns(ApiGroup):
    def get_ddns_list(self) -> GetResponseType:
        return self._connection.get('ddns/ddns-list')

    def get_status(self) -> GetResponseType:
        return self._connection.get('ddns/status')
