import enum


@enum.unique
class ResponseEnum(enum.Enum):
    OK = 'OK'


# not @enum.unique as long as the deprecated CSFR spelling is there
class ResponseCodeEnum(enum.IntEnum):
    ERROR_SYSTEM_UNKNOWN = 100001
    ERROR_SYSTEM_NO_SUPPORT = 100002
    ERROR_SYSTEM_NO_RIGHTS = 100003
    ERROR_SYSTEM_BUSY = 100004
    ERROR_SYSTEM_CSRF = 125002
    """Deprecated misspelling, use ERROR_SYSTEM_CSRF instead."""
    ERROR_SYSTEM_CSFR = ERROR_SYSTEM_CSRF
