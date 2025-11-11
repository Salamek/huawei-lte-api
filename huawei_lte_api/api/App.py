from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.exceptions import ResponseErrorException
from huawei_lte_api.Session import GetResponseType, SetResponseType


class App(ApiGroup):
    def operatorinfo(self, lang: str = "en_us") -> GetResponseType:
        """
        Get operator information.

        :param lang: Language code (default is 'en_us').
        :return: Operator information.

        Usage example:
        >>> app = App(session)
        >>> operator_info = app.operatorinfo()
        >>> print(operator_info)
        """
        return self._session.get("app/operatorinfo", {"lang": lang})

    def privacypolicy(self, lang: str = "en_us") -> GetResponseType:
        """
        Get privacy policy.

        :param lang: Language code (default is 'en_us').
        :return: Privacy policy.

        Usage example:
        >>> app = App(session)
        >>> privacy_policy = app.privacypolicy()
        >>> print(privacy_policy)
        """
        return self._session.get("app/privacypolicy", {"lang": lang})

    def accept_privacypolicy(self, approve: bool = False) -> SetResponseType:
        """
        Accept or decline the privacy policy.

        :param approve: Boolean indicating whether to approve the privacy policy (default is False).
        :return: "OK" if the operation is successful, raises ResponseErrorException otherwise.

        Usage example:
        >>> app = App(session)
        >>> response = app.accept_privacypolicy(approve=True)
        >>> print(response)
        """
        response = self._session.post_get("app/privacypolicy",
                                      {
                                          "data": {
                                              "Approve": "2" if approve else "0",
                                              "Liscence": "0",  # deliberate typo
                                          },
                                      },
                                      is_json=True)
        error_code = response["errcode"]
        if error_code == 0:
            return "OK"

        raise ResponseErrorException(
            message="Unexpected response: " + str(response),
            code=int(error_code),
        )
