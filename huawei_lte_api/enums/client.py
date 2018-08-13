import enum


@enum.unique
class ResponseEnum(enum.Enum):
    OK = 'OK'


@enum.unique
class ResponseCodeEnum(enum.IntEnum):
    ERROR_SYSTEM_UNKNOWN = 100001
    ERROR_SYSTEM_NO_SUPPORT = 100002
    ERROR_SYSTEM_NO_RIGHTS = 100003
    ERROR_SYSTEM_BUSY = 100004
    ERROR_SYSTEM_CSFR =  125002