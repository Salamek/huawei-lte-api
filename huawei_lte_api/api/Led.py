from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Led(ApiGroup):
    def nightmode(self) -> GetResponseType:
        """
        Get the status of the LED night mode.

        :return: LED night mode status.

        Usage example:
        >>> led = Led(session)
        >>> nightmode_status = led.nightmode()
        >>> print(nightmode_status)
        """
        return self._session.get("led/nightmode")

    def appctrlled(self) -> GetResponseType:
        """
        Get the status of the LED app control.

        :return: LED app control status.

        Usage example:
        >>> led = Led(session)
        >>> appctrlled_status = led.appctrlled()
        >>> print(appctrlled_status)
        """
        return self._session.get("led/appctrlled")
