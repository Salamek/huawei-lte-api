from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class App(ApiGroup):
    def operatorinfo(self, lang: str = 'en_us') -> GetResponseType:
        return self._session.get('app/operatorinfo', {'lang': lang})

    def privacypolicy(self, lang: str = 'en_us') -> GetResponseType:
        return self._session.get('app/privacypolicy', {'lang': lang})

    def accept_privacypolicy(self) -> GetResponseType:
        return self._session.post_get('app/privacypolicy', {"Approve": "2", "Liscence": "0"}, is_json=True)
