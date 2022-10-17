from typing import List, cast

from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class System(ApiGroup):
    def devcapacity(self) -> GetResponseType:
        return self._session.get('system/devcapacity')

    def deviceinfo(self) -> GetResponseType:
        return self._session.get('system/deviceinfo')

    def deviceinfoex(self) -> GetResponseType:
        return self._session.get('system/deviceinfoex')

    def onlineupg(self) -> GetResponseType:
        return self._session.post_get(
            'system/onlineupg',
            data={'action': 'check', 'data': {'UpdateAction': 1}},
            is_json=True,
        )

    def onlinestate(self, devid: str = 'all') -> List[GetResponseType]:
        return cast(
            List[GetResponseType],
            self._session.get('system/onlinestate', {'devid': devid})
        )

    def hostinfo(self) -> List[GetResponseType]:
        return cast(
            List[GetResponseType],
            self._session.get('system/HostInfo')
        )
