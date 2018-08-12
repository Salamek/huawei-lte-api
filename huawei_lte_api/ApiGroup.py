from huawei_lte_api.Connection import Connection


class ApiGroup(object):

    def __init__(self, connection: Connection):
        self._connection = connection
