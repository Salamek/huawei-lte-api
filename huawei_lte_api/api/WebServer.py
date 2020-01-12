from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class WebServer(ApiGroup):
    def publickey(self) -> GetResponseType:
        return self._connection.get('webserver/publickey')

    def token(self) -> GetResponseType:
        return self._connection.get('webserver/token')

    def white_list_switch(self) -> GetResponseType:
        return self._connection.get('webserver/white_list_switch')
