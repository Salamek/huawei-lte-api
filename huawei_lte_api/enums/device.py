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

    # Backups configuration, it can be downloaded later from http://192.168.8.1/nvram.bak
    # it is Base64 encoded nvram dump, you need to be authorized to download this file
    BACKUP_CONFIGURATION = 3
    POWER_OFF = 4


@enum.unique
class ModeEnum(enum.IntEnum):
    NORMAL = 0
    DEBUG = 1
    ENABLE_TELNET = 2
