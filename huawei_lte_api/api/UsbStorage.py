from huawei_lte_api.ApiGroup import ApiGroup


class UsbStorage(ApiGroup):

    def fsstatus(self) -> dict:
        return self._connection.get('usbstorage/fsstatus')

    def usbaccount(self) -> dict:
        return self._connection.get('usbstorage/usbaccount')
