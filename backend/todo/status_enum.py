from enum import Enum, auto


class Status(Enum):
    OPEN_STATUS = auto()
    IN_PROGRESS = auto()
    CLOSED = auto()
