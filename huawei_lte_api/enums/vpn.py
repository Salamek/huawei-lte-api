import enum


@enum.unique
class VPNType(enum.Enum):
    PPTP = 'pptp'
    L2TP = 'l2tp'
