from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType


class UsbPrinter(ApiGroup):

    def printerlist(self) -> GetResponseType:
        return self._session.get('usbprinter/printerlist')
