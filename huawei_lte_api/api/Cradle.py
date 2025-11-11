from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Cradle(ApiGroup):
    def status_info(self) -> GetResponseType:
        """
        Get cradle status information.

        :return: Cradle status information.

        Usage example:
        >>> cradle = Cradle(session)
        >>> status_info = cradle.status_info()
        >>> print(status_info)
        """
        return self._session.get("cradle/status-info")

    def feature_switch(self) -> GetResponseType:
        """
        Get cradle feature switch status.

        :return: Cradle feature switch status.

        Usage example:
        >>> cradle = Cradle(session)
        >>> feature_switch = cradle.feature_switch()
        >>> print(feature_switch)
        """
        return self._session.get("cradle/feature-switch")

    def basic_info(self) -> GetResponseType:
        """
        Get cradle basic information.

        :return: Cradle basic information.

        Usage example:
        >>> cradle = Cradle(session)
        >>> basic_info = cradle.basic_info()
        >>> print(basic_info)
        """
        return self._session.get("cradle/basic-info")

    def factory_mac(self) -> GetResponseType:
        """
        Get cradle factory MAC address.

        :return: Cradle factory MAC address.

        Usage example:
        >>> cradle = Cradle(session)
        >>> factory_mac = cradle.factory_mac()
        >>> print(factory_mac)
        """
        return self._session.get("cradle/factory-mac")

    def mac_info(self) -> GetResponseType:
        """
        Get cradle MAC address information.

        :return: Cradle MAC address information.

        Usage example:
        >>> cradle = Cradle(session)
        >>> mac_info = cradle.mac_info()
        >>> print(mac_info)
        """
        return self._session.get("cradle/mac-info")
