from huawei_lte_api.Client import Client


class Device(object):
    def __init__(self, connection: Client):
        self.connection = connection

    def information(self):
        return self.connection._get('device/information')