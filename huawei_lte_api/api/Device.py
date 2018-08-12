
from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class Device(ApiGroup):
    @authorized_call
    def information(self):
        return self.connection.get('device/information')

    def autorun_version(self):
        return self.connection.get('device/autorun-version')

    def device_feature_switch(self):
        return self.connection.get('device/device-feature-switch')

    def basic_information(self):
        return self.connection.get('device/basic_information')

    def usb_tethering_switch(self):
        return self.connection.get('device/usb-tethering-switch')