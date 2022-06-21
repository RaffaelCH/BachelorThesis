import unittest
from pathlib import Path

from codediffparser.parser import Parser
from codediffparser.mode import Mode


class TestTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        source_branch = str(Path(__file__).resolve().parent.joinpath('./source/test'))
        target_branch = str(Path(__file__).resolve().parent.joinpath('./target/test'))
        filter_files = ['simple_class_import.py']

        parser = Parser()
        parser.parse(target_branch, filter_files, Mode.TARGET)
        parser.parse(source_branch, filter_files, Mode.SOURCE)
        parser.graph.cleanup()
        cls.result = parser.graph


    def test_import_methodcall_link(self):
        try:
            link = self.result.links['METHOD_CALL:test.simple_class_import:test.simple_class.SimpleClass#test2033572573']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_import_method_link(self):
        try:
            link = self.result.links['METHOD:test.simple_class.SimpleClass:test.simple_class.SimpleClass#test2033572573']
        except KeyError:
            link = None
        self.assertIsNotNone(link)

    
    def test_type_reference_node(self):
        try:
            node = self.result.nodes['test.simple_class.SimpleClass']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_method_reference_node(self):
        try:
            node = self.result.nodes['test.simple_class.SimpleClass#test0']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    
    def test_complete_result_string(self):
        expected_output = r'{"links": [{"source": "test.simple_class_import", "target": "test.simple_class.SimpleClass#test2033572573", "relation": "METHOD_CALL", "status": "UNCHANGED", "id": "METHOD_CALL:test.simple_class_import:test.simple_class.SimpleClass#test2033572573"}, {"source": "test.simple_class.SimpleClass", "target": "test.simple_class.SimpleClass#test2033572573", "relation": "METHOD", "status": "UNCHANGED", "id": "METHOD:test.simple_class.SimpleClass:test.simple_class.SimpleClass#test2033572573"}], "nodes": [{"filePath": "test\\simple_class_import.py", "name": "simple_class_import", "declaringScopesName": null, "packageName": "test.simple_class_import", "type": "SCRIPT", "position": [], "positionOld": [], "status": "DELETED", "parentNodeId": null, "id": "test.simple_class_import", "generated": false, "language": "Python"}, {"filePath": "test\\simple_class.py", "name": "SimpleClass", "declaringScopesName": "", "packageName": "test.simple_class", "type": "TYPE_REFERENCE", "position": [5, 5], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.simple_class", "id": "test.simple_class.SimpleClass", "generated": false, "language": "Python"}, {"filePath": "test\\simple_class.py", "name": "test", "declaringScopesName": "SimpleClass", "packageName": "test.simple_class", "type": "METHOD_REFERENCE", "position": [5, 5], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.simple_class.SimpleClass", "id": "test.simple_class.SimpleClass#test0", "generated": false, "language": "Python"}]}'
        self.assertEqual(str(self.result), expected_output)