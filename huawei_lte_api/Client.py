from huawei_lte_api.Connection import Connection
from huawei_lte_api.api.User import User
from huawei_lte_api.api.Device import Device
from huawei_lte_api.api.OnlineUpdate import OnlineUpdate


class Client(object):
    def __init__(self, connection: Connection):
        self.user = User(connection)
        self.device = Device(connection)
        self.online_update = OnlineUpdate(connection)