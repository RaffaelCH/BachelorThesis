from .qualified_name_helper import QualifiedNameHelper
from .status import Status
from .node_type import NodeType


class Node():

    def __init__(self):
        self.file_path = ""
        self.name = ""
        self.declaring_classes_name = ""
        self.project_name = "" # == packageName
        self.type = NodeType.UNKNOWNFILE
        #self.modifiers = []
        self.position = [] # target: starting line, ending line
        self.position_old = [] # source: starting line, ending line
        self.status = Status.UNCHANGED
        self.parent_node_id = None
        self.param_hash_code = "0"
        self.node_hash_code = "0"
        self.is_generated = False
        self.language = "Python"
        self.notes = "" # Is used for error messages.
    
    
    def get_id(self):
        if self.type is NodeType.METHOD or self.type is NodeType.METHOD_REFERENCE:
            return QualifiedNameHelper.concat_save_with_delimiter("#", self.parent_node_id, self.name) + str(self.param_hash_code)
        elif self.type is NodeType.FUNCTION or self.type is NodeType.FUNCTION_REFERENCE:
            return QualifiedNameHelper.concat_save(self.project_name, self.declaring_classes_name, self.name) + str(self.param_hash_code)
        elif self.type is NodeType.SCRIPT:
            return self.project_name
        elif self.type is NodeType.UNKNOWNFILE:
            return self.file_path
        elif self.type is NodeType.TOOLERROR:
            return str(self.node_hash_code)
        else:
            return QualifiedNameHelper.concat_save(self.project_name, self.declaring_classes_name, self.name)

    
    def set_position(self, start_line, end_line):
        self.position = [start_line, end_line]

    def set_position_old(self, start_line, end_line):
        self.position_old = [start_line, end_line]
    

    def json_helper(self):
        """Export node to json."""
        obj = {}
        obj['filePath'] = self.file_path
        obj['name'] = self.name
        obj['declaringScopesName'] = self.declaring_classes_name
        obj['packageName'] = self.project_name
        obj['type'] = self.type.name
        #obj['modifiers'] = self.modifiers
        obj['position'] = self.position
        obj['positionOld'] = self.position_old
        obj['status'] = self.status.name
        obj['parentNodeId'] = self.parent_node_id
        obj['id'] = self.get_id()
        obj['paramHashCode'] = self.param_hash_code
        obj['nodeHashCode'] = self.node_hash_code
        obj['generated'] = self.is_generated
        obj['language'] = "" if self.type is NodeType.UNKNOWNFILE else "Python"
        obj['notes'] = self.notes
        return obj