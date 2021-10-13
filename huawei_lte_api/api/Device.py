import warnings
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType, SetResponseType
from huawei_lte_api.enums.device import AntennaTypeEnum, ControlModeEnum


class Device(ApiGroup):
    def information(self) -> GetResponseType:
        return self._session.get('device/information')

    def autorun_version(self) -> GetResponseType:
        return self._session.get('device/autorun-version')

    def device_feature_switch(self) -> GetResponseType:
        return self._session.get('device/device-feature-switch')

    def basic_information(self) -> GetResponseType:
        return self._session.get('device/basic_information')

    def basicinformation(self) -> GetResponseType:
        return self._session.get('device/basicinformation')

    def usb_tethering_switch(self) -> GetResponseType:
        return self._session.get('device/usb-tethering-switch')

    def boot_time(self) -> GetResponseType:
        return self._session.get('device/boot_time')

    def set_control(self, control: ControlModeEnum = ControlModeEnum.POWER_OFF) -> SetResponseType:
        """
        Controls powerstate of device
        :param control: ControlModeEnum REBOOT|POWER_OFF
        :return:
        """
        return self._session.post_set('device/control', {
            'Control': control.value
        })

    def signal(self) -> GetResponseType:
        return self._session.get('device/signal')

    def control(self, control: ControlModeEnum) -> SetResponseType:
        warnings.warn("device.control is deprecated, use device.set_control instead", DeprecationWarning)
        return self.set_control(control)

    def reboot(self) -> SetResponseType:
        warnings.warn("device.reboot is deprecated, use device.set_control(ControlModeEnum.REBOOT) instead", DeprecationWarning)
        return self.set_control(ControlModeEnum.REBOOT)

    def antenna_status(self) -> GetResponseType:
        return self._session.get('device/antenna_status')

    def get_antenna_settings(self) -> GetResponseType:
        return self._session.get('device/antenna_settings')

    def set_antenna_settings(self, antenna_type: AntennaTypeEnum = AntennaTypeEnum.AUTO) -> SetResponseType:
        return self._session.post_set('device/antenna_settings', {
            'antenna_type': antenna_type.value
        })

    def antenna_type(self) -> GetResponseType:
        return self._session.get('device/antenna_type')

    def antenna_set_type(self) -> GetResponseType:
        return self._session.get('device/antenna_set_type')

    def logsetting(self) -> GetResponseType:
        """
        Endpoint found by reverse engineering B310s-22 firmware, unknown usage
        :return:
        """
        return self._session.get('device/logsetting')
