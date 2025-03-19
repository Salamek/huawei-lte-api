from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType, SetResponseType


class Diagnosis(ApiGroup):
    def trace_route_result(self) -> GetResponseType:
        """
        Get the result of the traceroute diagnosis.

        :return: Traceroute result.

        Usage example:
        >>> diagnosis = Diagnosis(session)
        >>> traceroute_result = diagnosis.trace_route_result()
        >>> print(traceroute_result)
        """
        return self._session.get('diagnosis/tracerouteresult')

    def diagnose_ping(self) -> GetResponseType:
        """
        Get the result of the ping diagnosis.

        :return: Ping result.

        Usage example:
        >>> diagnosis = Diagnosis(session)
        >>> ping_result = diagnosis.diagnose_ping()
        >>> print(ping_result)
        """
        return self._session.get('diagnosis/diagnose_ping')

    def set_diagnose_ping(self, host: str, timeout: int = 4000) -> SetResponseType:
        """
        Set the parameters for the ping diagnosis.

        :param host: Host to ping.
        :param timeout: Timeout for the ping (default is 4000 ms).
        :return: Set response type.

        Usage example:
        >>> diagnosis = Diagnosis(session)
        >>> response = diagnosis.set_diagnose_ping(host="example.com", timeout=5000)
        >>> print(response)
        """
        return self._session.post_set('diagnosis/diagnose_ping', {
            "Host": host, 
            "Timeout": timeout
            }
        )

    def diagnose_traceroute(self) -> GetResponseType:
        """
        Get the result of the traceroute diagnosis.

        :return: Traceroute result.

        Usage example:
        >>> diagnosis = Diagnosis(session)
        >>> traceroute_result = diagnosis.diagnose_traceroute()
        >>> print(traceroute_result)
        """
        return self._session.get('diagnosis/diagnose_traceroute')

    def set_diagnose_traceroute(self, host: str, timeout: int = 4000, max_hop_count: int = 30) -> SetResponseType:
        """
        Set the parameters for the traceroute diagnosis.

        :param host: Host to traceroute.
        :param timeout: Timeout for the traceroute (default is 4000 ms).
        :param max_hop_count: Maximum hop count for the traceroute (default is 30).
        :return: Set response type.

        Usage example:
        >>> diagnosis = Diagnosis(session)
        >>> response = diagnosis.set_diagnose_traceroute(host="example.com", timeout=5000, max_hop_count=20)
        >>> print(response)
        """
        return self._session.post_set('diagnosis/diagnose_traceroute', {
            "Host": host, 
            "MaxHopCount": max_hop_count, 
            "Timeout": timeout
            }
        )

    def time_reboot(self) -> GetResponseType:
        """
        Get the time reboot status.

        :return: Time reboot status.

        Usage example:
        >>> diagnosis = Diagnosis(session)
        >>> time_reboot_status = diagnosis.time_reboot()
        >>> print(time_reboot_status)
        """
        return self._session.get('diagnosis/time_reboot')
