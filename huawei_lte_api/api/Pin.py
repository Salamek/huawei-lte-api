
from huawei_lte_api.ApiGroup import ApiGroup


class Pin(ApiGroup):
    def status(self) -> dict:
        return self._connection.get('pin/status')

    def simlock(self) -> dict:
        return self._connection.get('pin/simlock')

    def save_pin(self) -> dict:
        return self._connection.get('pin/save-pin')

    def operate(self, operate_type: int = 0, current_pin: int = None, new_pin: int = None, puk_code: int = None) -> dict:
        """
        Parameters
        ----------
        operate_type : int
            Operation type to perform (default is `0`).
            0 - verify PIN
            1 - enable PIN verification
            2 - disable PIN verification
            3 - set new PIN
            4 - use of the PUK code
        current_pin : int
            Current PIN number (default is `None`).
        new_pin : int
            New PIN number to set (default is `None`).
        puk_code : int
            PUK code to use in case it is required by the device (default is `None`).
        """
        dicttoxml_xargs = {
            'item_func': lambda x: x[:-1]
        }

        return self._connection.post('pin/operate', {
            'OperateType': operate_type,
            'CurrentPin': current_pin,
            'NewPin': new_pin,
            'PukCode': puk_code
        }, dicttoxml_xargs=dicttoxml_xargs)
