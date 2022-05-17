from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class System(ApiGroup):
    def devcapacity(self) -> GetResponseType:
        return self._session.get('system/devcapacity')

    def deviceinfo(self) -> GetResponseType:
        return self._session.get('system/deviceinfo')

    def onlineupg(self) -> GetResponseType:
        return self._session.post_get(
            'system/onlineupg',
            data={'action': 'check', 'data': {'UpdateAction': 1}},
            is_json=True,
        )
