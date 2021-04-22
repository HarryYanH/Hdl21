from enum import Enum


class PortDir(Enum):
    INPUT = 0
    OUTPUT = 1
    INOUT = 2
    NONE = 3


class SignalVisibility(Enum):
    INTERNAL = 0
    PORT = 1


class Signal:
    def __init__(
        self,
        *,
        name=None,
        width=1,
        visibility=SignalVisibility.INTERNAL,
        direction=PortDir.NONE,
    ):
        self.name = name
        self.width = width
        self.visibility = visibility
        self.direction = direction


def Input(**kwargs):
    return Signal(visibility=SignalVisibility.PORT, direction=PortDir.INPUT)


def Output(**kwargs):
    return Signal(visibility=SignalVisibility.PORT, direction=PortDir.OUTPUT)


def Inout(**kwargs):
    return Signal(visibility=SignalVisibility.PORT, direction=PortDir.INOUT)


def Port(**kwargs):
    return Signal(visibility=SignalVisibility.PORT, direction=PortDir.NONE)
