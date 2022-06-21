import unittest
from pathlib import Path

from codediffparser.parser import Parser
from codediffparser.mode import Mode


class TestTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        source_branch = str(Path(__file__).resolve().parent.joinpath('./source/test'))
        target_branch = str(Path(__file__).resolve().parent.joinpath('./target/test'))
        filter_files = ['simple_function.py']

        parser = Parser()
        parser.parse(target_branch, filter_files, Mode.TARGET)
        parser.parse(source_branch, filter_files, Mode.SOURCE)
        parser.graph.cleanup()
        cls.result = parser.graph


    def test_functioncall_from_function_link(self):
        try:
            link = self.result.links['FUNCTION_CALL:test.simple_function.foo3539003634:builtins.print2978873759']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_functioncall_link(self):
        try:
            link = self.result.links['FUNCTION_CALL:test.simple_function:test.simple_function.foo3539003634']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_functioncall2_link(self):
        try:
            link = self.result.links['FUNCTION_CALL:test.simple_function:test.simple_function.bar2607727064']
        except KeyError:
            link = None
        self.assertIsNotNone(link)

    
    def test_function_node(self):
        try:
            node = self.result.nodes['test.simple_function.foo3539003634']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_function2_node(self):
        try:
            node = self.result.nodes['test.simple_function.bar2607727064']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_bultin_function_reference_node(self):
        try:
            node = self.result.nodes['test.simple_function.foo737154539']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_script_node(self):
        try:
            node = self.result.nodes['test.simple_function']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    
    def test_complete_result_string(self):
        expected_output = r'{"links": [{"source": "test.simple_function.foo3539003634", "target": "builtins.print2978873759", "relation": "FUNCTION_CALL", "status": "UNCHANGED", "id": "FUNCTION_CALL:test.simple_function.foo3539003634:builtins.print2978873759"}, {"source": "test.simple_function", "target": "test.simple_function.foo3539003634", "relation": "FUNCTION_CALL", "status": "UNCHANGED", "id": "FUNCTION_CALL:test.simple_function:test.simple_function.foo3539003634"}, {"source": "test.simple_function", "target": "test.simple_function.bar2607727064", "relation": "FUNCTION_CALL", "status": "UNCHANGED", "id": "FUNCTION_CALL:test.simple_function:test.simple_function.bar2607727064"}], "nodes": [{"filePath": "test\\simple_function.py", "name": "foo", "declaringScopesName": "", "packageName": "test.simple_function", "type": "FUNCTION", "position": [1, 2], "positionOld": [1, 2], "status": "UNCHANGED", "parentNodeId": "test.simple_function", "id": "test.simple_function.foo3539003634", "generated": false, "language": "Python"}, {"filePath": null, "name": "print", "declaringScopesName": "", "packageName": "builtins", "type": "FUNCTION_REFERENCE", "position": [2, 2], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "builtins", "id": "builtins.print827027202", "generated": false, "language": "Python"}, {"filePath": "test\\simple_function.py", "name": "bar", "declaringScopesName": "", "packageName": "test.simple_function", "type": "FUNCTION", "position": [4, 5], "positionOld": [4, 5], "status": "UNCHANGED", "parentNodeId": "test.simple_function", "id": "test.simple_function.bar2607727064", "generated": false, "language": "Python"}, {"filePath": "test\\simple_function.py", "name": "foo", "declaringScopesName": "", "packageName": "test.simple_function", "type": "FUNCTION_REFERENCE", "position": [8, 8], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.simple_function", "id": "test.simple_function.foo737154539", "generated": false, "language": "Python"}, {"filePath": "test\\simple_function.py", "name": "simple_function", "declaringScopesName": null, "packageName": "test.simple_function", "type": "SCRIPT", "position": [], "positionOld": [], "status": "DELETED", "parentNodeId": null, "id": "test.simple_function", "generated": false, "language": "Python"}, {"filePath": "test\\simple_function.py", "name": "foo", "declaringScopesName": "", "packageName": "test.simple_function", "type": "FUNCTION_REFERENCE", "position": [9, 9], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.simple_function", "id": "test.simple_function.foo4239551527", "generated": false, "language": "Python"}, {"filePath": "test\\simple_function.py", "name": "bar", "declaringScopesName": "", "packageName": "test.simple_function", "type": "FUNCTION_REFERENCE", "position": [9, 9], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.simple_function", "id": "test.simple_function.bar0", "generated": false, "language": "Python"}]}'
        self.assertEqual(str(self.result), expected_output)