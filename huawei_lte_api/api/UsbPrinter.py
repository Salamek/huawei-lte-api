from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType


class UsbPrinter(ApiGroup):

    def printerlist(self) -> GetResponseType:
        return self._connection.get('usbprinter/printerlist')
