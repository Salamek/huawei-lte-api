import enum


@enum.unique
class PasswordTypeEnum(enum.IntEnum):
    BASE_64 = 0
    BASE_64_AFTER_PASSWORD_CHANGE = 3  # Im not sure about this name...
    SHA256 = 4


@enum.unique
class LoginErrorEnum(enum.IntEnum):
    USERNAME_WRONG = 108001
    PASSWORD_WRONG = 108002
    ALREADY_LOGIN = 108003
    USERNAME_PWD_WRONG = 108006
    USERNAME_PWD_OVERRUN = 108007
    USERNAME_PWD_MODIFY = 115002


@enum.unique
class LoginStateEnum(enum.IntEnum):
    LOGGED_IN = 0
    LOGGED_OUT = -1
    REPEAT = -2
