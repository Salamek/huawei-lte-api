
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class SNtp(ApiGroup):
    def get_settings(self) -> dict:
        return self._connection.get('sntp/settings')