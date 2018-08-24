import enum


@enum.unique
class ConnectionStatusEnum(enum.IntEnum):
    CONNECTING = 900
    CONNECTED = 901
    DISCONNECTED = 902
    DISCONNECTING = 903
    CONNECT_FAILED = 904
    CONNECT_STATUS_NULL = 905
    CONNECT_STATUS_ERROR = 906
