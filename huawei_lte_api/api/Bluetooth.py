from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Bluetooth(ApiGroup):
    def settings(self) -> GetResponseType:
        """
        Get Bluetooth settings.
        
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage.
        
        :return: Bluetooth settings.
        
        Usage example:
        >>> bluetooth = Bluetooth(session)
        >>> settings = bluetooth.settings()
        >>> print(settings)
        """
        return self._session.get('bluetooth/settings')

    def scan(self) -> GetResponseType:
        """
        Scan for Bluetooth devices.
        
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage.
        
        :return: Scan results.
        
        Usage example:
        >>> bluetooth = Bluetooth(session)
        >>> scan_results = bluetooth.scan()
        >>> print(scan_results)
        """
        return self._session.get('bluetooth/scan')
