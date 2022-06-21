import unittest
from pathlib import Path

from codediffparser.parser import Parser
from codediffparser.mode import Mode


class TestTest(unittest.TestCase):

    @classmethod
    def setUp(cls):
        source_branch = str(Path(__file__).resolve().parent.joinpath('./source/test'))
        target_branch = str(Path(__file__).resolve().parent.joinpath('./target/test'))
        filter_files = ['aliasing.py']

        parser = Parser()
        parser.parse(target_branch, filter_files, Mode.TARGET)
        parser.parse(source_branch, filter_files, Mode.SOURCE)
        parser.graph.cleanup()
        cls.result = parser.graph


    def test_methodcall_link(self):
        try:
            link = self.result.links['METHOD_CALL:test.aliasing:test.simple_class.SimpleClass#test2033572573']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_method_link(self):
        try:
            link = self.result.links['METHOD_CALL:test.aliasing:test.simple_class.SimpleClass#test2033572573']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_functioncall_link(self):
        try:
            link = self.result.links['FUNCTION_CALL:test.aliasing:test.simple_function.foo3539003634']
        except KeyError:
            link = None
        self.assertIsNotNone(link)

    
    def test_simple_class_script_node(self):
        try:
            node = self.result.nodes['test.aliasing']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_simple_class_reference_node(self):
        try:
            node = self.result.nodes['test.simple_class.SimpleClass']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_simple_class_method_reference_node(self):
        try:
            node = self.result.nodes['test.simple_class.SimpleClass#test0']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_simple_function_reference_node(self):
        try:
            node = self.result.nodes['test.simple_function.foo2193372843']
        except KeyError:
            node = None
        self.assertIsNotNone(node)

    
    def test_complete_result_string(self):
        expected_output = r'{"links": [{"source": "test.aliasing", "target": "test.simple_class.SimpleClass#test2033572573", "relation": "METHOD_CALL", "status": "UNCHANGED", "id": "METHOD_CALL:test.aliasing:test.simple_class.SimpleClass#test2033572573"}, {"source": "test.simple_class.SimpleClass", "target": "test.simple_class.SimpleClass#test2033572573", "relation": "METHOD", "status": "UNCHANGED", "id": "METHOD:test.simple_class.SimpleClass:test.simple_class.SimpleClass#test2033572573"}, {"source": "test.aliasing", "target": "test.simple_function.foo3539003634", "relation": "FUNCTION_CALL", "status": "UNCHANGED", "id": "FUNCTION_CALL:test.aliasing:test.simple_function.foo3539003634"}], "nodes": [{"filePath": "test\\aliasing.py", "name": "aliasing", "declaringScopesName": null, "packageName": "test.aliasing", "type": "SCRIPT", "position": [], "positionOld": [], "status": "UNCHANGED", "parentNodeId": null, "id": "test.aliasing", "generated": false, "language": "Python", "notes": ""}, {"filePath": "test\\simple_class.py", "name": "SimpleClass", "declaringScopesName": "", "packageName": "test.simple_class", "type": "TYPE_REFERENCE", "position": [6, 6], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.simple_class", "id": "test.simple_class.SimpleClass", "generated": false, "language": "Python", "notes": ""}, {"filePath": "test\\simple_class.py", "name": "test", "declaringScopesName": "SimpleClass", "packageName": "test.simple_class", "type": "METHOD_REFERENCE", "position": [6, 6], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.simple_class.SimpleClass", "id": "test.simple_class.SimpleClass#test0", "generated": false, "language": "Python", "notes": ""}, {"filePath": "test\\simple_function.py", "name": "foo", "declaringScopesName": "", "packageName": "test.simple_function", "type": "FUNCTION_REFERENCE", "position": [8, 8], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.simple_function", "id": "test.simple_function.foo2193372843", "generated": false, "language": "Python", "notes": ""}]}'
        self.assertEqual(str(self.result), expected_output)