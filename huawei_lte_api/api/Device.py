
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.enums.device import AntennaTypeEnum
from huawei_lte_api.AuthorizedConnection import authorized_call


class Device(ApiGroup):
    @authorized_call
    def information(self) ->dict:
        return self._connection.get('device/information')

    def autorun_version(self) ->dict:
        return self._connection.get('device/autorun-version')

    def device_feature_switch(self) ->dict:
        return self._connection.get('device/device-feature-switch')

    def basic_information(self) ->dict:
        return self._connection.get('device/basic_information')

    def usb_tethering_switch(self) ->dict:
        return self._connection.get('device/usb-tethering-switch')

    def boot_time(self) ->dict:
        return self._connection.get('device/boot_time')

    def set_control(self, control: int=4):
        return self._connection.post('device/control', {
            'Control': control
        })

    def signal(self) ->dict:
        return self._connection.get('device/signal')

    @authorized_call
    def control(self, control: int):
        return self._connection.post('device/control', {
            'Control': control
        })

    def reboot(self) -> dict:
        return self.control(1)

    def antenna_status(self) -> dict:
        return self._connection.get('device/antenna_status')

    def get_antenna_settings(self) -> dict:
        return self._connection.get('device/antenna_settings')

    def set_antenna_settings(self, antenna_type: AntennaTypeEnum=AntennaTypeEnum.AUTO) -> dict:
        return self._connection.post('device/antenna_settings', {
            'antenna_type': antenna_type.value
        })

    def antenna_type(self) -> dict:
        return self._connection.get('device/antenna_type')
