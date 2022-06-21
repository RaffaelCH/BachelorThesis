from enum import Enum, auto

class Status(Enum):
    ADDED = auto()
    DELETED = auto()
    CHANGED = auto()
    UNCHANGED = auto()