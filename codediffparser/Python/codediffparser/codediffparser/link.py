from .status import Status
from .link_relation import LinkRelation # define in this class?
from .qualified_name_helper import QualifiedNameHelper


class Link:
    
    def __init__(self):
        self.source = ""
        self.target = ""
        self.relation = None # TODO: add typing
        self.status = Status.UNCHANGED # TODO: add typing

    def get_id(self):
        relation_name = self.relation.name if self.relation else ""
        return QualifiedNameHelper.concat_save_with_delimiter(":", relation_name, self.source, self.target)
    
    def json_helper(self):
        obj = {}
        obj['source'] = self.source
        obj['target'] = self.target
        obj['relation'] = str(self.relation.name if self.relation else "")
        obj['status'] = self.status.name
        obj['id'] = self.get_id()
        return obj