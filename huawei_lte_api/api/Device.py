import warnings
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Session import GetResponseType, SetResponseType
from huawei_lte_api.enums.device import AntennaTypeEnum, ControlModeEnum, ModeEnum


class Device(ApiGroup):
    def information(self) -> GetResponseType:
        """
        Get device information.

        :return: Device information.

        Usage example:
        >>> device = Device(session)
        >>> info = device.information()
        >>> print(info)
        """
        return self._session.get('device/information')

    def autorun_version(self) -> GetResponseType:
        """
        Get autorun version.

        :return: Autorun version.

        Usage example:
        >>> device = Device(session)
        >>> version = device.autorun_version()
        >>> print(version)
        """
        return self._session.get('device/autorun-version')

    def device_feature_switch(self) -> GetResponseType:
        """
        Get device feature switch status.

        :return: Device feature switch status.

        Usage example:
        >>> device = Device(session)
        >>> feature_switch = device.device_feature_switch()
        >>> print(feature_switch)
        """
        return self._session.get('device/device-feature-switch')

    def basic_information(self) -> GetResponseType:
        """
        Get basic device information.

        :return: Basic device information.

        Usage example:
        >>> device = Device(session)
        >>> basic_info = device.basic_information()
        >>> print(basic_info)
        """
        return self._session.get('device/basic_information')

    def set_basic_information(self, restore_default_status: bool = False) -> SetResponseType:
        """
        Set basic device information.

        :param restore_default_status: Boolean indicating whether to restore default status (default is False).
        :return: Set response type.

        Usage example:
        >>> device = Device(session)
        >>> response = device.set_basic_information(restore_default_status=True)
        >>> print(response)
        """
        return self._session.post_set('device/basic_information',
                                      {
                                          "restore_default_status": 1 if restore_default_status else 0
                                      })

    def basicinformation(self) -> GetResponseType:
        """
        Get basic device information (alternative endpoint).

        :return: Basic device information.

        Usage example:
        >>> device = Device(session)
        >>> basic_info = device.basicinformation()
        >>> print(basic_info)
        """
        return self._session.get('device/basicinformation')

    def usb_tethering_switch(self) -> GetResponseType:
        """
        Get USB tethering switch status.

        :return: USB tethering switch status.

        Usage example:
        >>> device = Device(session)
        >>> tethering_switch = device.usb_tethering_switch()
        >>> print(tethering_switch)
        """
        return self._session.get('device/usb-tethering-switch')

    def boot_time(self) -> GetResponseType:
        """
        Get device boot time.

        :return: Device boot time.

        Usage example:
        >>> device = Device(session)
        >>> boot_time = device.boot_time()
        >>> print(boot_time)
        """
        return self._session.get('device/boot_time')

    def set_control(self, control: ControlModeEnum = ControlModeEnum.POWER_OFF) -> SetResponseType:
        """
        Controls power state of the device.

        :param control: ControlModeEnum (REBOOT|POWER_OFF).
        :return: Set response type.

        Usage example:
        >>> device = Device(session)
        >>> response = device.set_control(control=ControlModeEnum.REBOOT)
        >>> print(response)
        """
        return self._session.post_set('device/control', {
            'Control': control.value
        })

    def signal(self) -> GetResponseType:
        """
        Get device signal information.

        :return: Device signal information.

        Usage example:
        >>> device = Device(session)
        >>> signal_info = device.signal()
        >>> print(signal_info)
        """
        return self._session.get('device/signal')

    def control(self, control: ControlModeEnum) -> SetResponseType:
        """
        Deprecated: Use set_control instead.

        :param control: ControlModeEnum.
        :return: Set response type.

        Usage example:
        >>> device = Device(session)
        >>> response = device.control(control=ControlModeEnum.POWER_OFF)
        >>> print(response)
        """
        warnings.warn("device.control is deprecated, use device.set_control instead", DeprecationWarning)
        return self.set_control(control)

    def reboot(self) -> SetResponseType:
        """
        Deprecated: Use set_control(ControlModeEnum.REBOOT) instead.

        :return: Set response type.

        Usage example:
        >>> device = Device(session)
        >>> response = device.reboot()
        >>> print(response)
        """
        warnings.warn("device.reboot is deprecated, use device.set_control(ControlModeEnum.REBOOT) instead", DeprecationWarning)
        return self.set_control(ControlModeEnum.REBOOT)

    def antenna_status(self) -> GetResponseType:
        """
        Get device antenna status.

        :return: Device antenna status.

        Usage example:
        >>> device = Device(session)
        >>> antenna_status = device.antenna_status()
        >>> print(antenna_status)
        """
        return self._session.get('device/antenna_status')

    def get_antenna_settings(self) -> GetResponseType:
        """
        Get device antenna settings.

        :return: Device antenna settings.

        Usage example:
        >>> device = Device(session)
        >>> antenna_settings = device.get_antenna_settings()
        >>> print(antenna_settings)
        """
        return self._session.get('device/antenna_settings')

    def set_antenna_settings(self, antenna_type: AntennaTypeEnum = AntennaTypeEnum.AUTO) -> SetResponseType:
        """
        Set device antenna settings.

        :param antenna_type: AntennaTypeEnum (AUTO|INTERNAL|EXTERNAL).
        :return: Set response type.

        Usage example:
        >>> device = Device(session)
        >>> response = device.set_antenna_settings(antenna_type=AntennaTypeEnum.EXTERNAL)
        >>> print(response)
        """
        return self._session.post_set('device/antenna_settings', {
            'antenna_type': antenna_type.value
        })

    def antenna_type(self) -> GetResponseType:
        """
        Get device antenna type.

        :return: Device antenna type.

        Usage example:
        >>> device = Device(session)
        >>> antenna_type = device.antenna_type()
        >>> print(antenna_type)
        """
        return self._session.get('device/antenna_type')

    def antenna_set_type(self) -> GetResponseType:
        """
        Get device antenna set type.

        :return: Device antenna set type.

        Usage example:
        >>> device = Device(session)
        >>> antenna_set_type = device.antenna_set_type()
        >>> print(antenna_set_type)
        """
        return self._session.get('device/antenna_set_type')

    def logsetting(self) -> GetResponseType:
        """
        Get device log settings.

        Endpoint found by reverse engineering B310s-22 firmware, unknown usage.
        :return: Device log settings.

        Usage example:
        >>> device = Device(session)
        >>> log_settings = device.logsetting()
        >>> print(log_settings)
        """
        return self._session.get('device/logsetting')

    def logport(self) -> GetResponseType:
        """
        Get device log port.

        :return: Device log port.

        Usage example:
        >>> device = Device(session)
        >>> log_port = device.logport()
        >>> print(log_port)
        """
        return self._session.get('device/logport')

    def datalock(self) -> GetResponseType:
        """
        Get device data lock status.

        :return: Device data lock status.

        Usage example:
        >>> device = Device(session)
        >>> data_lock = device.datalock()
        >>> print(data_lock)
        """
        return self._session.get('device/datalock')

    def vendorname(self, lang: str = 'en_us') -> GetResponseType:
        """
        Get device vendor name.

        This endpoint is known to break the session with some devices
        that don't support it. Approach with care.

        :param lang: Language code (default is 'en_us').
        :return: Device vendor name.

        Usage example:
        >>> device = Device(session)
        >>> vendor_name = device.vendorname(lang='en_us')
        >>> print(vendor_name)
        """
        return self._session.post_get('device/vendorname', {
            'language': lang
        })

    def mode(self, mode: ModeEnum) -> SetResponseType:
        """
        Sets mode of the device, it can enable telnet, set debug mode or production mode, see ModeEnum.

        :param mode: ModeEnum.
        :return: Set response type.

        Usage example:
        >>> device = Device(session)
        >>> response = device.mode(mode=ModeEnum.DEBUG)
        >>> print(response)
        """
        return self._session.post_set('device/mode', {
            'mode': mode
        })

    def compress_logfile(self) -> GetResponseType:
        """
        Returns link to archived log file.

        :return: Link to archived log file.

        Usage example:
        >>> device = Device(session)
        >>> log_file_link = device.compress_logfile()
        >>> print(log_file_link)
        """
        return self._session.get('device/compresslogfile')
