import unittest
from pathlib import Path

from codediffparser.parser import Parser
from codediffparser.mode import Mode


class TestTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        source_branch = str(Path(__file__).resolve().parent.joinpath('./source/test'))
        target_branch = str(Path(__file__).resolve().parent.joinpath('./target/test'))
        filter_files = ['simple_class.py']

        parser = Parser()
        parser.parse(target_branch, filter_files, Mode.TARGET)
        parser.parse(source_branch, filter_files, Mode.SOURCE)
        parser.graph.cleanup()
        cls.result = parser.graph


    def test_init_method_link(self):
        try:
            link = self.result.links['METHOD:test.simple_class.SimpleClass:test.simple_class.SimpleClass#__init__3281279809']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_method_link(self):
        try:
            link = self.result.links['METHOD:test.simple_class.SimpleClass:test.simple_class.SimpleClass#test2033572573']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_methodcall_link(self):
        try:
            link = self.result.links['METHOD_CALL:test.simple_class:test.simple_class.SimpleClass#test2033572573']
        except KeyError:
            link = None
        self.assertIsNotNone(link)

    
    def test_class_node(self):
        try:
            node = self.result.nodes['test.simple_class.SimpleClass']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_init_method_node(self):
        try:
            node = self.result.nodes['test.simple_class.SimpleClass#__init__3281279809']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_method_node(self):
        try:
            node = self.result.nodes['test.simple_class.SimpleClass#test2033572573']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_methodcall_node(self):
        try:
            node = self.result.nodes['test.simple_class.SimpleClass#test0']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    
    def test_complete_result_string(self):
        expected_output = r'{"links": [{"source": "test.simple_class.SimpleClass", "target": "test.simple_class.SimpleClass#__init__3281279809", "relation": "METHOD", "status": "UNCHANGED", "id": "METHOD:test.simple_class.SimpleClass:test.simple_class.SimpleClass#__init__3281279809"}, {"source": "test.simple_class.SimpleClass", "target": "test.simple_class.SimpleClass#test2033572573", "relation": "METHOD", "status": "UNCHANGED", "id": "METHOD:test.simple_class.SimpleClass:test.simple_class.SimpleClass#test2033572573"}, {"source": "test.simple_class.SimpleClass#test2033572573", "target": "builtins.print2978873759", "relation": "FUNCTION_CALL", "status": "UNCHANGED", "id": "FUNCTION_CALL:test.simple_class.SimpleClass#test2033572573:builtins.print2978873759"}, {"source": "test.simple_class", "target": "test.simple_class.SimpleClass#test2033572573", "relation": "METHOD_CALL", "status": "UNCHANGED", "id": "METHOD_CALL:test.simple_class:test.simple_class.SimpleClass#test2033572573"}], "nodes": [{"filePath": "test\\simple_class.py", "name": "SimpleClass", "declaringScopesName": "", "packageName": "test.simple_class", "type": "CLASS", "position": [1, 7], "positionOld": [1, 7], "status": "UNCHANGED", "parentNodeId": "test.simple_class", "id": "test.simple_class.SimpleClass", "generated": false, "language": "Python"}, {"filePath": "test\\simple_class.py", "name": "__init__", "declaringScopesName": "SimpleClass", "packageName": "test.simple_class", "type": "METHOD", "position": [3, 4], "positionOld": [3, 4], "status": "UNCHANGED", "parentNodeId": "test.simple_class.SimpleClass", "id": "test.simple_class.SimpleClass#__init__3281279809", "generated": false, "language": "Python"}, {"filePath": "test\\simple_class.py", "name": "test", "declaringScopesName": "SimpleClass", "packageName": "test.simple_class", "type": "METHOD", "position": [6, 7], "positionOld": [6, 7], "status": "UNCHANGED", "parentNodeId": "test.simple_class.SimpleClass", "id": "test.simple_class.SimpleClass#test2033572573", "generated": false, "language": "Python"}, {"filePath": null, "name": "print", "declaringScopesName": "", "packageName": "builtins", "type": "FUNCTION_REFERENCE", "position": [7, 7], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "builtins", "id": "builtins.print4278384533", "generated": false, "language": "Python"}, {"filePath": "test\\simple_class.py", "name": "simple_class", "declaringScopesName": null, "packageName": "test.simple_class", "type": "SCRIPT", "position": [], "positionOld": [], "status": "DELETED", "parentNodeId": null, "id": "test.simple_class", "generated": false, "language": "Python"}, {"filePath": "test\\simple_class.py", "name": "test", "declaringScopesName": "SimpleClass", "packageName": "test.simple_class", "type": "METHOD_REFERENCE", "position": [11, 11], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.simple_class.SimpleClass", "id": "test.simple_class.SimpleClass#test0", "generated": false, "language": "Python"}]}'
        self.assertEqual(str(self.result), expected_output)