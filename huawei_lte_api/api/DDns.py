from huawei_lte_api.ApiGroup import ApiGroup


class DDns(ApiGroup):
    def get_ddns_list(self) -> dict:
        return self._connection.get('ddns/ddns-list')

    def get_status(self) ->dict:
        return self._connection.get('ddns/status')
