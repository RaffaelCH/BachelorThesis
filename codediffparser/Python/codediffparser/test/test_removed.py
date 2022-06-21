import unittest
from pathlib import Path

from codediffparser.parser import Parser
from codediffparser.mode import Mode


class TestTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        source_branch = str(Path(__file__).resolve().parent.joinpath('./source/test'))
        target_branch = str(Path(__file__).resolve().parent.joinpath('./target/test'))
        filter_files = ['removed.py']

        parser = Parser()
        parser.parse(target_branch, filter_files, Mode.TARGET)
        parser.parse(source_branch, filter_files, Mode.SOURCE)
        parser.graph.cleanup()
        cls.result = parser.graph


    def test_init_method_link(self):
        try:
            link = self.result.links['METHOD:test.removed.SimpleClass:test.removed.SimpleClass#__init__3281279809']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_method_link(self):
        try:
            link = self.result.links['METHOD:test.removed.SimpleClass:test.removed.SimpleClass#test2033572573']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_methodcall_link(self):
        try:
            link = self.result.links['METHOD_CALL:test.removed:test.removed.SimpleClass#test2033572573']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_functioncall_from_function_link(self):
        try:
            link = self.result.links['FUNCTION_CALL:test.removed.foo3539003634:builtins.print2978873759']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_functioncall_link(self):
        try:
            link = self.result.links['FUNCTION_CALL:test.removed:test.removed.foo3539003634']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_functioncall2_link(self):
        try:
            link = self.result.links['FUNCTION_CALL:test.removed:test.removed.bar2607727064']
        except KeyError:
            link = None
        self.assertIsNotNone(link)

    
    def test_class_node(self):
        try:
            node = self.result.nodes['test.removed.SimpleClass']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_init_method_node(self):
        try:
            node = self.result.nodes['test.removed.SimpleClass#__init__3281279809']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_method_node(self):
        try:
            node = self.result.nodes['test.removed.SimpleClass#test2033572573']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_methodcall_node(self):
        try:
            node = self.result.nodes['test.removed.SimpleClass#test0']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_function_node(self):
        try:
            node = self.result.nodes['test.removed.foo3539003634']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_function2_node(self):
        try:
            node = self.result.nodes['test.removed.bar2607727064']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_bultin_function_reference_node(self):
        try:
            node = self.result.nodes['test.removed.foo737154539']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_script_node(self):
        try:
            node = self.result.nodes['test.removed']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    
    def test_complete_result_string(self):
        expected_output = r'{"links": [{"source": "test.removed.SimpleClass", "target": "test.removed.SimpleClass#__init__3281279809", "relation": "METHOD", "status": "DELETED", "id": "METHOD:test.removed.SimpleClass:test.removed.SimpleClass#__init__3281279809"}, {"source": "test.removed.SimpleClass", "target": "test.removed.SimpleClass#test2033572573", "relation": "METHOD", "status": "DELETED", "id": "METHOD:test.removed.SimpleClass:test.removed.SimpleClass#test2033572573"}, {"source": "test.removed.SimpleClass#test2033572573", "target": "builtins.print2978873759", "relation": "FUNCTION_CALL", "status": "DELETED", "id": "FUNCTION_CALL:test.removed.SimpleClass#test2033572573:builtins.print2978873759"}, {"source": "test.removed", "target": "test.removed.SimpleClass#test2033572573", "relation": "METHOD_CALL", "status": "DELETED", "id": "METHOD_CALL:test.removed:test.removed.SimpleClass#test2033572573"}, {"source": "test.removed.foo3539003634", "target": "builtins.print2978873759", "relation": "FUNCTION_CALL", "status": "DELETED", "id": "FUNCTION_CALL:test.removed.foo3539003634:builtins.print2978873759"}, {"source": "test.removed", "target": "test.removed.foo3539003634", "relation": "FUNCTION_CALL", "status": "DELETED", "id": "FUNCTION_CALL:test.removed:test.removed.foo3539003634"}, {"source": "test.removed", "target": "test.removed.bar2607727064", "relation": "FUNCTION_CALL", "status": "DELETED", "id": "FUNCTION_CALL:test.removed:test.removed.bar2607727064"}], "nodes": [{"filePath": "test\\removed.py", "name": "SimpleClass", "declaringScopesName": "", "packageName": "test.removed", "type": "CLASS", "position": [1, 7], "positionOld": [], "status": "DELETED", "parentNodeId": "test.removed", "id": "test.removed.SimpleClass", "generated": false, "language": "Python"}, {"filePath": "test\\removed.py", "name": "__init__", "declaringScopesName": "SimpleClass", "packageName": "test.removed", "type": "METHOD", "position": [3, 4], "positionOld": [], "status": "DELETED", "parentNodeId": "test.removed.SimpleClass", "id": "test.removed.SimpleClass#__init__3281279809", "generated": false, "language": "Python"}, {"filePath": "test\\removed.py", "name": "test", "declaringScopesName": "SimpleClass", "packageName": "test.removed", "type": "METHOD", "position": [6, 7], "positionOld": [], "status": "DELETED", "parentNodeId": "test.removed.SimpleClass", "id": "test.removed.SimpleClass#test2033572573", "generated": false, "language": "Python"}, {"filePath": null, "name": "print", "declaringScopesName": "", "packageName": "builtins", "type": "FUNCTION_REFERENCE", "position": [7, 7], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "builtins", "id": "builtins.print4278384533", "generated": false, "language": "Python"}, {"filePath": "test\\removed.py", "name": "removed", "declaringScopesName": null, "packageName": "test.removed", "type": "SCRIPT", "position": [], "positionOld": [], "status": "DELETED", "parentNodeId": null, "id": "test.removed", "generated": false, "language": "Python"}, {"filePath": "test\\removed.py", "name": "test", "declaringScopesName": "SimpleClass", "packageName": "test.removed", "type": "METHOD_REFERENCE", "position": [11, 11], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.removed.SimpleClass", "id": "test.removed.SimpleClass#test0", "generated": false, "language": "Python"}, {"filePath": "test\\removed.py", "name": "foo", "declaringScopesName": "", "packageName": "test.removed", "type": "FUNCTION", "position": [15, 16], "positionOld": [], "status": "DELETED", "parentNodeId": "test.removed", "id": "test.removed.foo3539003634", "generated": false, "language": "Python"}, {"filePath": null, "name": "print", "declaringScopesName": "", "packageName": "builtins", "type": "FUNCTION_REFERENCE", "position": [16, 16], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "builtins", "id": "builtins.print827027202", "generated": false, "language": "Python"}, {"filePath": "test\\removed.py", "name": "bar", "declaringScopesName": "", "packageName": "test.removed", "type": "FUNCTION", "position": [18, 19], "positionOld": [], "status": "DELETED", "parentNodeId": "test.removed", "id": "test.removed.bar2607727064", "generated": false, "language": "Python"}, {"filePath": "test\\removed.py", "name": "foo", "declaringScopesName": "", "packageName": "test.removed", "type": "FUNCTION_REFERENCE", "position": [22, 22], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.removed", "id": "test.removed.foo737154539", "generated": false, "language": "Python"}, {"filePath": "test\\removed.py", "name": "foo", "declaringScopesName": "", "packageName": "test.removed", "type": "FUNCTION_REFERENCE", "position": [23, 23], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.removed", "id": "test.removed.foo4239551527", "generated": false, "language": "Python"}, {"filePath": "test\\removed.py", "name": "bar", "declaringScopesName": "", "packageName": "test.removed", "type": "FUNCTION_REFERENCE", "position": [23, 23], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.removed", "id": "test.removed.bar0", "generated": false, "language": "Python"}]}'
        self.assertEqual(str(self.result), expected_output)