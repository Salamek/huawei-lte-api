from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType, SetResponseType


class Language(ApiGroup):
    def set_current_language(self, current_language: str) -> SetResponseType:
        """
        Set the current language.

        :param current_language: Language code to set as current.
        :return: Set response type.

        Usage example:
        >>> language = Language(session)
        >>> response = language.set_current_language(current_language='en_us')
        >>> print(response)
        """
        return self._session.post_set(
            "language/current-language",
            {
                "CurrentLanguage": current_language,
            },
        )

    def current_language(self) -> GetResponseType:
        """
        Get the current language.

        :return: Current language.

        Usage example:
        >>> language = Language(session)
        >>> current_lang = language.current_language()
        >>> print(current_lang)
        """
        return self._session.get("language/current-language")
