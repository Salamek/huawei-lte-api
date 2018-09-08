from huawei_lte_api.ApiGroup import ApiGroup


class UsbPrinter(ApiGroup):

    def printerlist(self) -> dict:
        return self._connection.get('usbprinter/printerlist')
