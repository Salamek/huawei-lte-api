
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class Diagnosis(ApiGroup):
    def trace_route_result(self) -> dict:
        return self._connection.get('diagnosis/tracerouteresult')
