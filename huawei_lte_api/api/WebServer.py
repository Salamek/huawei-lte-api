
from huawei_lte_api.ApiGroup import ApiGroup


class WebServer(ApiGroup):
    def publickey(self) -> dict:
        return self._connection.get('webserver/publickey')

    def token(self) -> dict:
        return self._connection.get('webserver/token')

    def white_list_switch(self) -> dict:
        return self._connection.get('webserver/white_list_switch')
