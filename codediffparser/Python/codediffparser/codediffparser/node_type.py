from enum import Enum, auto


class NodeType(Enum):

    CLASS = auto()
    METHOD = auto()
    FUNCTION = auto()
    TYPE_REFERENCE = auto() # class reference
    METHOD_REFERENCE = auto()
    FUNCTION_REFERENCE = auto()
    SCRIPT = auto()
    TOOLERROR = auto()
    UNKNOWNFILE = auto()


    def is_declared_type(self):
        if self is NodeType.CLASS or self is NodeType.METHOD or self is NodeType.FUNCTION:
            return True
        return False
    
    def is_referenced_type(self):
        if self is NodeType.TYPE_REFERENCE or self is NodeType.METHOD_REFERENCE or self is NodeType.FUNCTION_REFERENCE:
            return True
        return False