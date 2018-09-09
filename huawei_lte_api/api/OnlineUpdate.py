from huawei_lte_api.ApiGroup import ApiGroup
from huawei_lte_api.AuthorizedConnection import authorized_call


class OnlineUpdate(ApiGroup):
    def check_new_version(self) -> dict:
        return self._connection.get('online-update/check-new-version')

    @authorized_call
    def set_check_new_version(self) -> dict:
        return self._connection.post('online-update/check-new-version')

    def status(self) -> dict:
        return self._connection.get('online-update/status')

    def url_list(self) -> dict:
        return self._connection.get('online-update/url-list')

    def ack_newversion(self) -> dict:
        return self._connection.get('online-update/ack-newversion')

    def set_ack_newversion(self):
        return self._connection.post('online-update/ack-newversion', {
            'userAckNewVersion': 0
        })

    def cancel_downloading(self) -> dict:
        return self._connection.get('online-update/cancel-downloading')

    def set_cancel_downloading(self):
        return self._connection.post('online-update/cancel-downloading')

    def upgrade_messagebox(self) -> dict:
        return self._connection.get('online-update/upgrade-messagebox')

    def set_upgrade_messagebox(self, messagebox):
        return self._connection.post('online-update/upgrade-messagebox', {
            'messagebox': messagebox
        })

    def configuration(self) -> dict:
        return self._connection.get('online-update/configuration')

    def autoupdate_config(self) -> dict:
        return self._connection.get('online-update/autoupdate-config')
