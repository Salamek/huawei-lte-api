from huawei_lte_api.ApiGroup import ApiGroup


class Cwmp(ApiGroup):
    def basic_info(self) -> dict:
        return self._connection.get('cwmp/basic-info')
