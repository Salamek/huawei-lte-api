from __future__ import annotations

from typing import TYPE_CHECKING

from huawei_lte_api.ApiGroup import ApiGroup

if TYPE_CHECKING:
    from huawei_lte_api.Session import GetResponseType, SetResponseType

class Pin(ApiGroup):
    def status(self) -> GetResponseType:
        """
        Get the status of the PIN.

        :return: PIN status.

        Usage example:
        >>> pin = Pin(session)
        >>> pin_status = pin.status()
        >>> print(pin_status)
        """
        return self._session.get("pin/status")

    def simlock(self) -> GetResponseType:
        """
        Get the status of the SIM lock.

        :return: SIM lock status.

        Usage example:
        >>> pin = Pin(session)
        >>> simlock_status = pin.simlock()
        >>> print(simlock_status)
        """
        return self._session.get("pin/simlock")

    def save_pin(self) -> GetResponseType:
        """
        Save the PIN.

        :return: Save PIN response.

        Usage example:
        >>> pin = Pin(session)
        >>> save_pin_response = pin.save_pin()
        >>> print(save_pin_response)
        """
        return self._session.get("pin/save-pin")

    def operate(self, operate_type: str = "0", current_pin: str | None = None,
                new_pin: str | None = None, puk_code: str | None = None) \
            -> SetResponseType:
        """
        Perform an operation on the PIN.

        :param operate_type: Operation type to perform (default is `0`).
            0 - verify PIN
            1 - enable PIN verification
            2 - disable PIN verification
            3 - set new PIN
            4 - use of the PUK code
        :param current_pin: Current PIN number (default is `None`).
        :param new_pin: New PIN number to set (default is `None`).
        :param puk_code: PUK code to use in case it is required by the device (default is `None`).
        :return: Set response type.

        Usage example:
        >>> pin = Pin(session)
        >>> response = pin.operate(operate_type="1", current_pin="1234")
        >>> print(response)
        """
        return self._session.post_set("pin/operate", {
            "OperateType": operate_type,
            "CurrentPin": current_pin,
            "NewPin": new_pin,
            "PukCode": puk_code,
        }, is_encrypted=True)
