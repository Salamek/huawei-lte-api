from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType, SetResponseType
from huawei_lte_api.exceptions import ResponseErrorException


class App(ApiGroup):
    def operatorinfo(self, lang: str = 'en_us') -> GetResponseType:
        return self._session.get('app/operatorinfo', {'lang': lang})

    def privacypolicy(self, lang: str = 'en_us') -> GetResponseType:
        return self._session.get('app/privacypolicy', {'lang': lang})

    def accept_privacypolicy(self, approve: bool = False) -> SetResponseType:
        response = self._session.post_get('app/privacypolicy',
                                      {
                                          "data": {
                                              "Approve": "2" if approve else "0",
                                              "Liscence": "0"  # deliberate typo
                                          }
                                      },
                                      is_json=True)
        error_code = response["errcode"]
        if error_code == 0:
            return "OK"

        raise ResponseErrorException(
            message="Unexpected response: " + str(response),
            code=int(error_code)
        )
