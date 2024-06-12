from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType, SetResponseType


class Diagnosis(ApiGroup):
    def trace_route_result(self) -> GetResponseType:
        return self._session.get('diagnosis/tracerouteresult')

    def diagnose_ping(self) -> GetResponseType:
        return self._session.get('diagnosis/diagnose_ping')

    def set_diagnose_ping(self, host: str, timeout: int = 4000) -> SetResponseType:
        return self._session.post_set('diagnosis/diagnose_ping', {
            "Host": host, 
            "Timeout": timeout
            }
        )

    def diagnose_traceroute(self) -> GetResponseType:
        return self._session.get('diagnosis/diagnose_traceroute')

    def set_diagnose_traceroute(self, host: str, timeout: int = 4000, max_hop_count: int = 30) -> SetResponseType:
        return self._session.post_set('diagnosis/diagnose_traceroute', {
            "Host": host, 
            "MaxHopCount": max_hop_count, 
            "Timeout": timeout
            }
        )

    def time_reboot(self) -> GetResponseType:
        return self._session.get('diagnosis/time_reboot')
