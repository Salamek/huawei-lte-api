from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class Ussd(ApiGroup):

    def status(self) -> GetResponseType:
        return self._session.get('ussd/status')

    def get(self) -> GetResponseType:
        return self._session.get('ussd/get')

    def send(self, content: str) -> GetResponseType:
        return self._session.post_get('ussd/send', {
            'content': content,
            'codeType': 'codeType',
            'timeout': None
        })
