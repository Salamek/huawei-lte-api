from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.Connection import GetResponseType, SetResponseType


class OnlineUpdate(ApiGroup):
    def check_new_version(self) -> GetResponseType:
        return self._connection.get('online-update/check-new-version')

    def set_check_new_version(self) -> SetResponseType:
        return self._connection.post_set('online-update/check-new-version')

    def status(self) -> GetResponseType:
        return self._connection.get('online-update/status')

    def url_list(self) -> GetResponseType:
        return self._connection.get('online-update/url-list')

    def ack_newversion(self) -> GetResponseType:
        return self._connection.get('online-update/ack-newversion')

    def set_ack_newversion(self) -> SetResponseType:
        return self._connection.post_set('online-update/ack-newversion', {
            'userAckNewVersion': 0
        })

    def cancel_downloading(self) -> GetResponseType:
        """
        Invoking this method is known to cause some devices to reboot.
        """
        return self._connection.get('online-update/cancel-downloading')

    def set_cancel_downloading(self) -> SetResponseType:
        return self._connection.post_set('online-update/cancel-downloading')

    def upgrade_messagebox(self) -> GetResponseType:
        return self._connection.get('online-update/upgrade-messagebox')

    def set_upgrade_messagebox(self, messagebox: str) -> SetResponseType:
        return self._connection.post_set('online-update/upgrade-messagebox', {
            'messagebox': messagebox
        })

    def configuration(self) -> GetResponseType:
        return self._connection.get('online-update/configuration')

    def autoupdate_config(self) -> GetResponseType:
        return self._connection.get('online-update/autoupdate-config')

    def redirect_cancel(self) -> GetResponseType:
        return self._connection.get('online-update/redirect_cancel')
