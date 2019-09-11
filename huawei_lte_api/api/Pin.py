
from huawei_lte_api.ApiGroup import ApiGroup


class Pin(ApiGroup):
    def status(self) -> dict:
        return self._connection.get('pin/status')

    def simlock(self) -> dict:
        return self._connection.get('pin/simlock')

    def save_pin(self) -> dict:
        return self._connection.get('pin/save-pin')
    
    def enter_pin(self, pin: int) -> dict:
        dicttoxml_xargs = {
            'item_func': lambda x: x[:-1]
        }

        return self._connection.post('pin/operate', {
            'OperateType': 0,
            'CurrentPin': pin,
            'NewPin': '',
            'PukCode': ''
        }, dicttoxml_xargs=dicttoxml_xargs)
