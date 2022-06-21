import unittest
from pathlib import Path

from codediffparser.parser import Parser
from codediffparser.mode import Mode


class TestTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        source_branch = str(Path(__file__).resolve().parent.joinpath('./source/test'))
        target_branch = str(Path(__file__).resolve().parent.joinpath('./target/test'))
        filter_files = ['nested_function.py']

        parser = Parser()
        parser.parse(target_branch, filter_files, Mode.TARGET)
        parser.parse(source_branch, filter_files, Mode.SOURCE)
        parser.graph.cleanup()
        cls.result = parser.graph


    def test_inner_function_link(self):
        try:
            link = self.result.links['FUNCTION:test.nested_function.foo3344688307:test.nested_function.foo.bar2607727064']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
        
    def test_inner_functioncall_link(self):
        try:
            link = self.result.links['FUNCTION_CALL:test.nested_function.foo3344688307:test.nested_function.foo.bar2607727064']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
        
    def test_outer_functioncall_link(self):
        try:
            link = self.result.links['FUNCTION_CALL:test.nested_function:test.nested_function.foo3344688307']
        except KeyError:
            link = None
        self.assertIsNotNone(link)

    
    def test_outer_function_node(self):
        try:
            node = self.result.nodes['test.nested_function.foo3344688307']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_inner_function_node(self):
        try:
            node = self.result.nodes['test.nested_function.foo.bar2607727064']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_inner_function_reference_node(self):
        try:
            node = self.result.nodes['test.nested_function.foo.bar0']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_script_node(self):
        try:
            node = self.result.nodes['test.nested_function.foo0']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    
    def test_complete_result_string(self):
        expected_output = r'{"links": [{"source": "test.nested_function.foo3344688307", "target": "test.nested_function.foo.bar2607727064", "relation": "FUNCTION", "status": "UNCHANGED", "id": "FUNCTION:test.nested_function.foo3344688307:test.nested_function.foo.bar2607727064"}, {"source": "test.nested_function.foo.bar2607727064", "target": "builtins.print2978873759", "relation": "FUNCTION_CALL", "status": "UNCHANGED", "id": "FUNCTION_CALL:test.nested_function.foo.bar2607727064:builtins.print2978873759"}, {"source": "test.nested_function.foo3344688307", "target": "test.nested_function.foo.bar2607727064", "relation": "FUNCTION_CALL", "status": "UNCHANGED", "id": "FUNCTION_CALL:test.nested_function.foo3344688307:test.nested_function.foo.bar2607727064"}, {"source": "test.nested_function", "target": "test.nested_function.foo3344688307", "relation": "FUNCTION_CALL", "status": "UNCHANGED", "id": "FUNCTION_CALL:test.nested_function:test.nested_function.foo3344688307"}], "nodes": [{"filePath": "test\\nested_function.py", "name": "foo", "declaringScopesName": "", "packageName": "test.nested_function", "type": "FUNCTION", "position": [1, 6], "positionOld": [1, 6], "status": "UNCHANGED", "parentNodeId": "test.nested_function", "id": "test.nested_function.foo3344688307", "generated": false, "language": "Python"}, {"filePath": "test\\nested_function.py", "name": "bar", "declaringScopesName": "foo", "packageName": "test.nested_function", "type": "FUNCTION", "position": [3, 4], "positionOld": [3, 4], "status": "UNCHANGED", "parentNodeId": "test.nested_function.foo3344688307", "id": "test.nested_function.foo.bar2607727064", "generated": false, "language": "Python"}, {"filePath": null, "name": "print", "declaringScopesName": "", "packageName": "builtins", "type": "FUNCTION_REFERENCE", "position": [4, 4], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "builtins", "id": "builtins.print2997445376", "generated": false, "language": "Python"}, {"filePath": "test\\nested_function.py", "name": "bar", "declaringScopesName": "foo", "packageName": "test.nested_function", "type": "FUNCTION_REFERENCE", "position": [6, 6], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.nested_function.foo3344688307", "id": "test.nested_function.foo.bar0", "generated": false, "language": "Python"}, {"filePath": "test\\nested_function.py", "name": "foo", "declaringScopesName": "", "packageName": "test.nested_function", "type": "FUNCTION_REFERENCE", "position": [9, 9], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.nested_function", "id": "test.nested_function.foo0", "generated": false, "language": "Python"}, {"filePath": "test\\nested_function.py", "name": "nested_function", "declaringScopesName": null, "packageName": "test.nested_function", "type": "SCRIPT", "position": [], "positionOld": [], "status": "DELETED", "parentNodeId": null, "id": "test.nested_function", "generated": false, "language": "Python"}]}'
        self.assertEqual(str(self.result), expected_output)