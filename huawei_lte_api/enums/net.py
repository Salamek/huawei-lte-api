import enum


@enum.unique
class NetworkModeEnum(enum.Enum):
    MODE_AUTO = '00'
    MODE_2G_ONLY = '01'
    MODE_3G_ONLY = '02'
    MODE_4G_ONLY = '03'
    MODE_4G_3G_AUTO = '0302'


@enum.unique
class NetworkBandEnum(enum.IntEnum):
    BC0A = 0x01
    BC0B = 0x02
    BC1 = 0x04
    BC2 = 0x08
    BC3 = 0x10
    BC4 = 0x20
    BC5 = 0x40
    GSM1800 = 0x80
    GSM900 = 0x300
    BC6 = 0x400
    BC7 = 0x800
    BC8 = 0x1000
    BC9 = 0x2000
    BC10 = 0x4000
    BC11 = 0x8000
    GSM850 = 0x80000
    GSM1900 = 0x200000
    UMTS_B1_2100 = 0x400000
    UMTS_B2_1900 = 0x800000
    BC12 = 0x10000000
    BC13 = 0x20000000
    UMTS_B5_850 = 0x4000000
    BC14 = 0x80000000
    UMTS_B8_900 = 0x2000000000000

    ALL = 0x3fffffff
    """Use alone, do not 'or' this with others."""


@enum.unique
class LTEBandEnum(enum.IntEnum):
    """For other values besides ALL, see set_net_mode docs."""
    ALL = 0x7fffffffffffffff
    """Use alone, do not 'or' this with others."""
