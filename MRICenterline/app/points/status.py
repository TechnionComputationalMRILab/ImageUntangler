from enum import Enum, auto


class TimerStatus(Enum):
    RUNNING = auto()
    STOPPED = auto()
    PAUSED = auto()


class PickerStatus(Enum):
    NOT_PICKING = auto()
    PICKING_MPR = auto()
    PICKING_LENGTH = auto()
    MODIFYING_MPR = auto()
    MODIFYING_LENGTH = auto()
    FIND_MPR = auto()
    FIND_LENGTH = auto()
    PICKING_MPR_PAIR = auto()


class PointStatus(Enum):
    LENGTH = auto()
    MPR = auto()
    LENGTH_IN_MPR = auto()

