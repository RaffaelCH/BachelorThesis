import unittest
from pathlib import Path

from codediffparser.parser import Parser
from codediffparser.mode import Mode


class TestTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        source_branch = str(Path(__file__).resolve().parent.joinpath('./source/test'))
        target_branch = str(Path(__file__).resolve().parent.joinpath('./target/test'))
        filter_files = ['added.py']

        parser = Parser()
        parser.parse(target_branch, filter_files, Mode.TARGET)
        parser.parse(source_branch, filter_files, Mode.SOURCE)
        parser.graph.cleanup()
        cls.result = parser.graph


    def test_init_method_link(self):
        try:
            link = self.result.links['METHOD:test.added.SimpleClass:test.added.SimpleClass#__init__3281279809']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_method_link(self):
        try:
            link = self.result.links['METHOD:test.added.SimpleClass:test.added.SimpleClass#test2033572573']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_methodcall_link(self):
        try:
            link = self.result.links['METHOD_CALL:test.added:test.added.SimpleClass#test2033572573']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_functioncall_from_function_link(self):
        try:
            link = self.result.links['FUNCTION_CALL:test.added.foo3539003634:builtins.print2978873759']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_functioncall_link(self):
        try:
            link = self.result.links['FUNCTION_CALL:test.added:test.added.foo3539003634']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_functioncall2_link(self):
        try:
            link = self.result.links['FUNCTION_CALL:test.added:test.added.bar2607727064']
        except KeyError:
            link = None
        self.assertIsNotNone(link)

    
    def test_class_node(self):
        try:
            node = self.result.nodes['test.added.SimpleClass']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_init_method_node(self):
        try:
            node = self.result.nodes['test.added.SimpleClass#__init__3281279809']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_method_node(self):
        try:
            node = self.result.nodes['test.added.SimpleClass#test2033572573']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_methodcall_node(self):
        try:
            node = self.result.nodes['test.added.SimpleClass#test0']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_function_node(self):
        try:
            node = self.result.nodes['test.added.foo3539003634']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_function2_node(self):
        try:
            node = self.result.nodes['test.added.bar2607727064']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_bultin_function_reference_node(self):
        try:
            node = self.result.nodes['test.added.foo737154539']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_script_node(self):
        try:
            node = self.result.nodes['test.added']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    
    def test_complete_result_string(self):
        expected_output = r'{"links": [{"source": "test.added.SimpleClass", "target": "test.added.SimpleClass#__init__3281279809", "relation": "METHOD", "status": "ADDED", "id": "METHOD:test.added.SimpleClass:test.added.SimpleClass#__init__3281279809"}, {"source": "test.added.SimpleClass", "target": "test.added.SimpleClass#test2033572573", "relation": "METHOD", "status": "ADDED", "id": "METHOD:test.added.SimpleClass:test.added.SimpleClass#test2033572573"}, {"source": "test.added.SimpleClass#test2033572573", "target": "builtins.print2978873759", "relation": "FUNCTION_CALL", "status": "ADDED", "id": "FUNCTION_CALL:test.added.SimpleClass#test2033572573:builtins.print2978873759"}, {"source": "test.added", "target": "test.added.SimpleClass#test2033572573", "relation": "METHOD_CALL", "status": "ADDED", "id": "METHOD_CALL:test.added:test.added.SimpleClass#test2033572573"}, {"source": "test.added.foo3539003634", "target": "builtins.print2978873759", "relation": "FUNCTION_CALL", "status": "ADDED", "id": "FUNCTION_CALL:test.added.foo3539003634:builtins.print2978873759"}, {"source": "test.added", "target": "test.added.foo3539003634", "relation": "FUNCTION_CALL", "status": "ADDED", "id": "FUNCTION_CALL:test.added:test.added.foo3539003634"}, {"source": "test.added", "target": "test.added.bar2607727064", "relation": "FUNCTION_CALL", "status": "ADDED", "id": "FUNCTION_CALL:test.added:test.added.bar2607727064"}], "nodes": [{"filePath": "test\\added.py", "name": "SimpleClass", "declaringScopesName": "", "packageName": "test.added", "type": "CLASS", "position": [1, 7], "positionOld": [], "status": "ADDED", "parentNodeId": "test.added", "id": "test.added.SimpleClass", "generated": false, "language": "Python", "notes": ""}, {"filePath": "test\\added.py", "name": "__init__", "declaringScopesName": "SimpleClass", "packageName": "test.added", "type": "METHOD", "position": [3, 4], "positionOld": [], "status": "ADDED", "parentNodeId": "test.added.SimpleClass", "id": "test.added.SimpleClass#__init__3281279809", "generated": false, "language": "Python", "notes": ""}, {"filePath": "test\\added.py", "name": "test", "declaringScopesName": "SimpleClass", "packageName": "test.added", "type": "METHOD", "position": [6, 7], "positionOld": [], "status": "ADDED", "parentNodeId": "test.added.SimpleClass", "id": "test.added.SimpleClass#test2033572573", "generated": false, "language": "Python", "notes": ""}, {"filePath": null, "name": "print", "declaringScopesName": "", "packageName": "builtins", "type": "FUNCTION_REFERENCE", "position": [7, 7], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "builtins", "id": "builtins.print4278384533", "generated": false, "language": "Python", "notes": ""}, {"filePath": "test\\added.py", "name": "added", "declaringScopesName": null, "packageName": "test.added", "type": "SCRIPT", "position": [], "positionOld": [], "status": "CHANGED", "parentNodeId": null, "id": "test.added", "generated": false, "language": "Python", "notes": ""}, {"filePath": "test\\added.py", "name": "test", "declaringScopesName": "SimpleClass", "packageName": "test.added", "type": "METHOD_REFERENCE", "position": [11, 11], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.added.SimpleClass", "id": "test.added.SimpleClass#test0", "generated": false, "language": "Python", "notes": ""}, {"filePath": "test\\added.py", "name": "foo", "declaringScopesName": "", "packageName": "test.added", "type": "FUNCTION", "position": [15, 16], "positionOld": [], "status": "ADDED", "parentNodeId": "test.added", "id": "test.added.foo3539003634", "generated": false, "language": "Python", "notes": ""}, {"filePath": null, "name": "print", "declaringScopesName": "", "packageName": "builtins", "type": "FUNCTION_REFERENCE", "position": [16, 16], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "builtins", "id": "builtins.print827027202", "generated": false, "language": "Python", "notes": ""}, {"filePath": "test\\added.py", "name": "bar", "declaringScopesName": "", "packageName": "test.added", "type": "FUNCTION", "position": [18, 19], "positionOld": [], "status": "ADDED", "parentNodeId": "test.added", "id": "test.added.bar2607727064", "generated": false, "language": "Python", "notes": ""}, {"filePath": "test\\added.py", "name": "foo", "declaringScopesName": "", "packageName": "test.added", "type": "FUNCTION_REFERENCE", "position": [22, 22], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.added", "id": "test.added.foo737154539", "generated": false, "language": "Python", "notes": ""}, {"filePath": "test\\added.py", "name": "foo", "declaringScopesName": "", "packageName": "test.added", "type": "FUNCTION_REFERENCE", "position": [23, 23], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.added", "id": "test.added.foo4239551527", "generated": false, "language": "Python", "notes": ""}, {"filePath": "test\\added.py", "name": "bar", "declaringScopesName": "", "packageName": "test.added", "type": "FUNCTION_REFERENCE", "position": [23, 23], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.added", "id": "test.added.bar0", "generated": false, "language": "Python", "notes": ""}]}'
        self.assertEqual(str(self.result), expected_output)