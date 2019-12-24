from huawei_lte_api.Connection import Connection
from huawei_lte_api.Connection import GetResponseType, SetResponseType  # pylint: disable=unused-import


class ApiGroup:

    def __init__(self, connection: Connection):
        self._connection = connection
