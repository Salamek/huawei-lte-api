
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class Diagnosis(ApiGroup):
    def trace_route_result(self) -> dict:
        return self._connection.get('diagnosis/tracerouteresult')

    def diagnose_ping(self) -> dict:
        return self._connection.get('diagnosis/diagnose_ping')

    def set_diagnose_ping(self, host: str, timeout: int = 4000):
        return self._connection.post('diagnosis/diagnose_ping', dict(
            Host=host,
            Timeout=timeout,
        ))

    def diagnose_traceroute(self) -> dict:
        return self._connection.get('diagnosis/diagnose_traceroute')

    def set_diagnose_traceroute(self, host: str, timeout: int = 4000, max_hop_count: int = 30):
        return self._connection.post('diagnosis/diagnose_ping', dict(
            Host=host,
            MaxHopCount=max_hop_count,
            Timeout=timeout,
        ))

    def time_reboot(self) -> dict:
        return self._connection.get('diagnosis/time_reboot')
