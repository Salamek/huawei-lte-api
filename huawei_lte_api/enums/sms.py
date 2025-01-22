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
    UNKNOWN = 4  # SMS i send to my self have this save mode set, SMS from operator have savemode=1


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
    UNKNOWN = 4  # No idea what this is but all send SMS from UI has this priority


@enum.unique
class TypeEnum(enum.IntEnum):
    SINGLE = 1
    MULTIPART = 2
    UNICODE = 5  # Not sure
    DELIVERY_CONFIRMATION_SUCCESS = 7
    DELIVERY_CONFIRMATION_FAILURE = 8


@enum.unique
class StatusEnum(enum.IntEnum):
    NEW = 0
    READ = 1
    PENDING = 2  # Not sure
    SEND = 3  # Not sure
    SEND_FAILED = 4


@enum.unique
class SortTypeEnum(enum.IntEnum):
    DATE = 0
    PHONE = 1
    INDEX = 2
