from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Developer(ApiGroup):
    def developermode_featureswitch(self) -> GetResponseType:
        """
        Get the status of the developer mode feature switch.

        :return: Developer mode feature switch status.

        Usage example:
        >>> developer = Developer(session)
        >>> featureswitch_status = developer.developermode_featureswitch()
        >>> print(featureswitch_status)
        """
        return self._session.get("developer/developermode-featureswitch")

    def atport_status(self) -> GetResponseType:
        """
        Get the status of the AT port.

        :return: AT port status.

        Usage example:
        >>> developer = Developer(session)
        >>> atport_status = developer.atport_status()
        >>> print(atport_status)
        """
        return self._session.get("app/atport-status")
