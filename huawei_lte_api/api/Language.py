from huawei_lte_api.ApiGroup import ApiGroup, GetResponseType, SetResponseType


class Language(ApiGroup):
    def set_current_language(self, current_language: str) -> SetResponseType:
        return self._connection.post_set('language/current-language', {
            'CurrentLanguage': current_language
        })

    def current_language(self) -> GetResponseType:
        return self._connection.get('language/current-language')
