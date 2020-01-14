from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType, SetResponseType
from huawei_lte_api.enums.device import AntennaTypeEnum


class Device(ApiGroup):
    def information(self) -> GetResponseType:
        return self._connection.get('device/information')

    def autorun_version(self) -> GetResponseType:
        return self._connection.get('device/autorun-version')

    def device_feature_switch(self) -> GetResponseType:
        return self._connection.get('device/device-feature-switch')

    def basic_information(self) -> GetResponseType:
        return self._connection.get('device/basic_information')

    def basicinformation(self) -> GetResponseType:
        return self._connection.get('device/basicinformation')

    def usb_tethering_switch(self) -> GetResponseType:
        return self._connection.get('device/usb-tethering-switch')

    def boot_time(self) -> GetResponseType:
        return self._connection.get('device/boot_time')

    def set_control(self, control: int=4) -> SetResponseType:
        return self._connection.post_set('device/control', {
            'Control': control
        })

    def signal(self) -> GetResponseType:
        return self._connection.get('device/signal')

    def control(self, control: int) -> SetResponseType:
        return self._connection.post_set('device/control', {
            'Control': control
        })

    def reboot(self) -> SetResponseType:
        return self.control(1)

    def antenna_status(self) -> GetResponseType:
        return self._connection.get('device/antenna_status')

    def get_antenna_settings(self) -> GetResponseType:
        return self._connection.get('device/antenna_settings')

    def set_antenna_settings(self, antenna_type: AntennaTypeEnum=AntennaTypeEnum.AUTO) -> SetResponseType:
        return self._connection.post_set('device/antenna_settings', {
            'antenna_type': antenna_type.value
        })

    def antenna_type(self) -> GetResponseType:
        return self._connection.get('device/antenna_type')

    def antenna_set_type(self) -> GetResponseType:
        return self._connection.get('device/antenna_set_type')

    def logsetting(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._connection.get('device/logsetting')
