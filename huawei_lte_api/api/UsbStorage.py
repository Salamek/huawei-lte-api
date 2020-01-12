from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class UsbStorage(ApiGroup):

    def fsstatus(self) -> GetResponseType:
        return self._connection.get('usbstorage/fsstatus')

    def usbaccount(self) -> GetResponseType:
        return self._connection.get('usbstorage/usbaccount')
