import enum


@enum.unique
class BoxTypeEnum(enum.IntEnum):
    LOCAL_INBOX = 1
    LOCAL_SENT = 2
    LOCAL_DRAFT = 3
    LOCAL_TRASH = 4
    SIM_INBOX = 5
    SIM_SENT = 6
    SIM_DRAFT = 7
    MIX_INBOX = 8
    MIX_SENT = 9
    MIX_DRAFT = 10


@enum.unique
class TextModeEnum(enum.IntEnum):
    UCS2 = 0
    SEVEN_BIT = 1
    EIGHT_BIT = 2


@enum.unique
class SaveModeEnum(enum.IntEnum):
    LOCAL = 0
    SIM_CARD = 1
    SIM_CARD_FIRST = 2
    LOCAL_FIRST = 3


@enum.unique
class SendTypeEnum(enum.IntEnum):
    SEND = 0
    SEND_AND_SAVE = 1


@enum.unique
class PriorityEnum(enum.IntEnum):
    NORMAL = 0
    INTERACTIVE = 1
    URGENT = 2
    EMERGENCY = 3