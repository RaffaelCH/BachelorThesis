import unittest
from pathlib import Path

from codediffparser.parser import Parser
from codediffparser.mode import Mode


class TestTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        source_branch = str(Path(__file__).resolve().parent.joinpath('./source/test'))
        target_branch = str(Path(__file__).resolve().parent.joinpath('./target/test'))
        filter_files = ['simple_inheritance.py']

        parser = Parser()
        parser.parse(target_branch, filter_files, Mode.TARGET)
        parser.parse(source_branch, filter_files, Mode.SOURCE)
        parser.graph.cleanup()
        cls.result = parser.graph


    def test_super_method_link(self):
        try:
            link = self.result.links['METHOD:test.simple_inheritance.SuperInheritance:test.simple_inheritance.SuperInheritance#super_inheritance2456482305']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_superclass_link(self):
        try:
            link = self.result.links['SUPERCLASS:test.simple_inheritance.InheritanceClass:test.simple_inheritance.SuperInheritance']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_sub_method_link(self):
        try:
            link = self.result.links['METHOD:test.simple_inheritance.InheritanceClass:test.simple_inheritance.InheritanceClass#inherit231315594']
        except KeyError:
            link = None
        self.assertIsNotNone(link)

    def test_sub_methodcall_link(self):
        try:
            link = self.result.links['METHOD_CALL:test.simple_inheritance:test.simple_inheritance.InheritanceClass#inherit231315594']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
        
    def test_inherited_methodcall_link(self):
        try:
            link = self.result.links['METHOD_CALL:test.simple_inheritance:test.simple_inheritance.SuperInheritance#super_inheritance2456482305']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    

    def test_superclass_node(self):
        try:
            node = self.result.nodes['test.simple_inheritance.SuperInheritance']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_super_method_node(self):
        try:
            node = self.result.nodes['test.simple_inheritance.SuperInheritance#super_inheritance2456482305']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_subclass_node(self):
        try:
            node = self.result.nodes['test.simple_inheritance.InheritanceClass']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_sub_method_node(self):
        try:
            node = self.result.nodes['test.simple_inheritance.InheritanceClass#inherit231315594']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    
    def test_complete_result_string(self):
        expected_output = r'{"links": [{"source": "test.simple_inheritance.SuperInheritance", "target": "test.simple_inheritance.SuperInheritance#super_inheritance2456482305", "relation": "METHOD", "status": "UNCHANGED", "id": "METHOD:test.simple_inheritance.SuperInheritance:test.simple_inheritance.SuperInheritance#super_inheritance2456482305"}, {"source": "test.simple_inheritance.SuperInheritance#super_inheritance2456482305", "target": "builtins.print2978873759", "relation": "FUNCTION_CALL", "status": "UNCHANGED", "id": "FUNCTION_CALL:test.simple_inheritance.SuperInheritance#super_inheritance2456482305:builtins.print2978873759"}, {"source": "test.simple_inheritance.InheritanceClass", "target": "test.simple_inheritance.SuperInheritance", "relation": "SUPERCLASS", "status": "UNCHANGED", "id": "SUPERCLASS:test.simple_inheritance.InheritanceClass:test.simple_inheritance.SuperInheritance"}, {"source": "test.simple_inheritance.InheritanceClass", "target": "test.simple_inheritance.InheritanceClass#inherit231315594", "relation": "METHOD", "status": "UNCHANGED", "id": "METHOD:test.simple_inheritance.InheritanceClass:test.simple_inheritance.InheritanceClass#inherit231315594"}, {"source": "test.simple_inheritance.InheritanceClass#inherit231315594", "target": "builtins.print2978873759", "relation": "FUNCTION_CALL", "status": "UNCHANGED", "id": "FUNCTION_CALL:test.simple_inheritance.InheritanceClass#inherit231315594:builtins.print2978873759"}, {"source": "test.simple_inheritance", "target": "test.simple_inheritance.InheritanceClass#inherit231315594", "relation": "METHOD_CALL", "status": "UNCHANGED", "id": "METHOD_CALL:test.simple_inheritance:test.simple_inheritance.InheritanceClass#inherit231315594"}, {"source": "test.simple_inheritance", "target": "test.simple_inheritance.SuperInheritance#super_inheritance2456482305", "relation": "METHOD_CALL", "status": "UNCHANGED", "id": "METHOD_CALL:test.simple_inheritance:test.simple_inheritance.SuperInheritance#super_inheritance2456482305"}], "nodes": [{"filePath": "test\\simple_inheritance.py", "name": "SuperInheritance", "declaringScopesName": "", "packageName": "test.simple_inheritance", "type": "CLASS", "position": [1, 4], "positionOld": [1, 4], "status": "UNCHANGED", "parentNodeId": "test.simple_inheritance", "id": "test.simple_inheritance.SuperInheritance", "generated": false, "language": "Python"}, {"filePath": "test\\simple_inheritance.py", "name": "super_inheritance", "declaringScopesName": "SuperInheritance", "packageName": "test.simple_inheritance", "type": "METHOD", "position": [3, 4], "positionOld": [3, 4], "status": "UNCHANGED", "parentNodeId": "test.simple_inheritance.SuperInheritance", "id": "test.simple_inheritance.SuperInheritance#super_inheritance2456482305", "generated": false, "language": "Python"}, {"filePath": null, "name": "print", "declaringScopesName": "", "packageName": "builtins", "type": "FUNCTION_REFERENCE", "position": [4, 4], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "builtins", "id": "builtins.print663222420", "generated": false, "language": "Python"}, {"filePath": "test\\simple_inheritance.py", "name": "InheritanceClass", "declaringScopesName": "", "packageName": "test.simple_inheritance", "type": "CLASS", "position": [7, 10], "positionOld": [7, 10], "status": "UNCHANGED", "parentNodeId": "test.simple_inheritance", "id": "test.simple_inheritance.InheritanceClass", "generated": false, "language": "Python"}, {"filePath": "test\\simple_inheritance.py", "name": "inherit", "declaringScopesName": "InheritanceClass", "packageName": "test.simple_inheritance", "type": "METHOD", "position": [9, 10], "positionOld": [9, 10], "status": "UNCHANGED", "parentNodeId": "test.simple_inheritance.InheritanceClass", "id": "test.simple_inheritance.InheritanceClass#inherit231315594", "generated": false, "language": "Python"}, {"filePath": null, "name": "print", "declaringScopesName": "", "packageName": "builtins", "type": "FUNCTION_REFERENCE", "position": [10, 10], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "builtins", "id": "builtins.print2306457844", "generated": false, "language": "Python"}, {"filePath": "test\\simple_inheritance.py", "name": "simple_inheritance", "declaringScopesName": null, "packageName": "test.simple_inheritance", "type": "SCRIPT", "position": [], "positionOld": [], "status": "DELETED", "parentNodeId": null, "id": "test.simple_inheritance", "generated": false, "language": "Python"}, {"filePath": "test\\simple_inheritance.py", "name": "inherit", "declaringScopesName": "InheritanceClass", "packageName": "test.simple_inheritance", "type": "METHOD_REFERENCE", "position": [14, 14], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.simple_inheritance.InheritanceClass", "id": "test.simple_inheritance.InheritanceClass#inherit0", "generated": false, "language": "Python"}, {"filePath": "test\\simple_inheritance.py", "name": "super_inheritance", "declaringScopesName": "SuperInheritance", "packageName": "test.simple_inheritance", "type": "METHOD_REFERENCE", "position": [15, 15], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.simple_inheritance.SuperInheritance", "id": "test.simple_inheritance.SuperInheritance#super_inheritance0", "generated": false, "language": "Python"}]}'
        self.assertEquals(str(self.result), expected_output)