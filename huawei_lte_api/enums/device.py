import enum


@enum.unique
class AntennaTypeEnum(enum.IntEnum):
    INTEGRATED = 0
    EXTERNAL_1_AND_2 = 1
    EXTERNAL_1 = 2
    AUTO = 3


@enum.unique
class ControlModeEnum(enum.IntEnum):
    REBOOT = 1
    RESET = 2  # Resets device into factory settings
    POWER_OFF = 4


@enum.unique
class ModeEnum(enum.IntEnum):
    NORMAL = 0
    DEBUG = 1
    ENABLE_TELNET = 2
