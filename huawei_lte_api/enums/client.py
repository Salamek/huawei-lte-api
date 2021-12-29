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
    ERROR_FORMAT_ERROR = 100005
    ERROR_VOICE_BUSY = 120001  # Unused
    ERROR_WRONG_TOKEN = 125001  # Unused
    ERROR_SYSTEM_CSRF = 125002
    ERROR_WRONG_SESSION_TOKEN = 125003  # Unused
