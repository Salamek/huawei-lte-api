import enum


@enum.unique
class AuthModeEnum(enum.Enum):
    AUTO = 'AUTO'
    OPEN = 'OPEN'
    SHARE = 'SHARE'
    WPA_PSK = 'WPA-PSK'
    WPA2_PSK = 'WPA2-PSK'
    WPA_WPA2_PSK = 'WPA/WPA2-PSK'


@enum.unique
class WpaEncryptModeEnum(enum.Enum):
    AES = 'AES'
    TKIP = 'TKIP'
    MIX = 'MIX'


@enum.unique
class WepEncryptModeEnum(enum.Enum):
    NONE = 'NONE'
    WEP = 'WEP'
    WEP64 = 'WEP64'
    WEP128 = 'WEP128'
