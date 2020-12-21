import enum


@enum.unique
class NetworkModeEnum(enum.Enum):
    MODE_AUTO = '00'
    MODE_2G_ONLY = '01'
    MODE_3G_ONLY = '02'
    MODE_4G_ONLY = '03'
    MODE_4G_3G_AUTO = '0302'
