
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class Language(ApiGroup):
    def set_current_language(self, current_language: str):
        return self._connection.post('language/current-language', {
            'CurrentLanguage': current_language
        })
