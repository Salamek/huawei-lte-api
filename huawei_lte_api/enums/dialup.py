import enum


class AuthModeEnum(enum.IntEnum):
    AUTO = 0
    PAP = 1
    CHAP = 2


class IpType(enum.IntEnum):
    IPV4 = 0
    IPV6 = 1
    IPV4_IPV6 = 2
