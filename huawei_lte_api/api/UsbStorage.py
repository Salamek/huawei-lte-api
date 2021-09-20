from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class UsbStorage(ApiGroup):

    def fsstatus(self) -> GetResponseType:
        return self._session.get('usbstorage/fsstatus')

    def usbaccount(self) -> GetResponseType:
        return self._session.get('usbstorage/usbaccount')
