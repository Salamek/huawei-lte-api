import enum

@enum.unique
class VPNType(enum.Enum):
    PPTP = 'PPTP'
    L2TP = 'L2TP'