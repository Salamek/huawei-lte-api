
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class Device(ApiGroup):
    @authorized_call
    def information(self):
        return self._connection.get('device/information')

    def autorun_version(self):
        return self._connection.get('device/autorun-version')

    def device_feature_switch(self):
        return self._connection.get('device/device-feature-switch')

    def basic_information(self):
        return self._connection.get('device/basic_information')

    def usb_tethering_switch(self):
        return self._connection.get('device/usb-tethering-switch')

    def boot_time(self):
        return self._connection.get('device/boot_time')

    def set_control(self, control: int=4):
        return self._connection.post('device/control', {
            'Control': control
        })