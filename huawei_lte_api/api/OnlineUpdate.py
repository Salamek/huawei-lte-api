from huawei_lte_api.ApiGroup import ApiGroup


class OnlineUpdate(ApiGroup):
    def check_new_version(self):
        return self.connection.get('online-update/check-new-version')

    def status(self):
        return self.connection.get('online-update/status')

    def url_list(self):
        return self.connection.get('online-update/url-list')

    def ack_newversion(self):
        return self.connection.get('online-update/ack-newversion')

    def cancel_downloading(self):
        return self.connection.get('online-update/cancel-downloading')