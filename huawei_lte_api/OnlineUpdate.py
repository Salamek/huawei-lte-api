from huawei_lte_api.Client import Client


class OnlineUpdate(object):
    def __init__(self, connection: Client):
        self.connection = connection

    def check_new_version(self):
        return self.connection._get('online-update/check-new-version')