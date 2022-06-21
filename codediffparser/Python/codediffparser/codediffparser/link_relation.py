from enum import Enum, auto

class LinkRelation(Enum):
    SUPERCLASS = auto()
    ENCLOSING_CLASS = auto()
    METHOD = auto()
    METHOD_CALL = auto()
    FUNCTION = auto()
    FUNCTION_CALL = auto()
    TOOLERROR = auto()
    #TYPE = 5 # Currently not used.