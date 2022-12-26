import enum


@enum.unique
class SdCardStatus(enum.IntEnum):
    NOT_DETECTED = 0
    OK = 1
    NOT_FORMATTED = 2
