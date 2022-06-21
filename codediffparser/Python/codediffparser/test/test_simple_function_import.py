import unittest
from pathlib import Path

from codediffparser.parser import Parser
from codediffparser.mode import Mode


class TestTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        source_branch = str(Path(__file__).resolve().parent.joinpath('./source/test'))
        target_branch = str(Path(__file__).resolve().parent.joinpath('./target/test'))
        filter_files = ['simple_function_import.py']

        parser = Parser()
        parser.parse(target_branch, filter_files, Mode.TARGET)
        parser.parse(source_branch, filter_files, Mode.SOURCE)
        parser.graph.cleanup()
        cls.result = parser.graph


    def test_functioncall_link(self):
        try:
            link = self.result.links['FUNCTION_CALL:test.simple_function_import:test.simple_function.foo3539003634']
        except KeyError:
            link = None
        self.assertIsNotNone(link)

    
    def test_function_reference_node(self):
        try:
            node = self.result.nodes['test.simple_function.foo2997445376']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_script_node(self):
        try:
            node = self.result.nodes['test.simple_function_import']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    
    def test_complete_result_string(self):
        expected_output = r'{"links": [{"source": "test.simple_function_import", "target": "test.simple_function.foo3539003634", "relation": "FUNCTION_CALL", "status": "UNCHANGED", "id": "FUNCTION_CALL:test.simple_function_import:test.simple_function.foo3539003634"}], "nodes": [{"filePath": "test\\simple_function.py", "name": "foo", "declaringScopesName": "", "packageName": "test.simple_function", "type": "FUNCTION_REFERENCE", "position": [3, 3], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.simple_function", "id": "test.simple_function.foo2997445376", "generated": false, "language": "Python"}, {"filePath": "test\\simple_function_import.py", "name": "simple_function_import", "declaringScopesName": null, "packageName": "test.simple_function_import", "type": "SCRIPT", "position": [], "positionOld": [], "status": "DELETED", "parentNodeId": null, "id": "test.simple_function_import", "generated": false, "language": "Python"}]}'
        self.assertEqual(str(self.result), expected_output)