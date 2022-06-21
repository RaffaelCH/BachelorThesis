import unittest
from pathlib import Path

from codediffparser.parser import Parser
from codediffparser.mode import Mode


class TestTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        source_branch = str(Path(__file__).resolve().parent.joinpath('./source/test'))
        target_branch = str(Path(__file__).resolve().parent.joinpath('./target/test'))
        filter_files = ['function_parameter_error.py']

        parser = Parser()
        parser.parse(target_branch, filter_files, Mode.TARGET)
        parser.parse(source_branch, filter_files, Mode.SOURCE)
        parser.graph.cleanup()
        cls.result = parser.graph


    def test_error_link(self):
        try:
            link = self.result.links['TOOLERROR:test.function_parameter_error:591271464']
        except KeyError:
            link = None
        self.assertIsNotNone(link)

    
    def test_function_node(self):
        try:
            node = self.result.nodes['test.function_parameter_error.fun40250162']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_script_node(self):
        try:
            node = self.result.nodes['test.function_parameter_error']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_error_node(self):
        try:
            node = self.result.nodes['591271464']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    
    def test_complete_result_string(self):
        expected_output = r'{"links": [{"source": "test.function_parameter_error", "target": "591271464", "relation": "TOOLERROR", "status": "UNCHANGED", "id": "TOOLERROR:test.function_parameter_error:591271464"}], "nodes": [{"filePath": "test\\function_parameter_error.py", "name": "fun", "declaringScopesName": "", "packageName": "test.function_parameter_error", "type": "FUNCTION", "position": [1, 2], "positionOld": [1, 2], "status": "UNCHANGED", "parentNodeId": "test.function_parameter_error", "id": "test.function_parameter_error.fun40250162", "generated": false, "language": "Python", "notes": ""}, {"filePath": "test\\function_parameter_error.py", "name": "function_parameter_error", "declaringScopesName": null, "packageName": "test.function_parameter_error", "type": "SCRIPT", "position": [], "positionOld": [], "status": "UNCHANGED", "parentNodeId": null, "id": "test.function_parameter_error", "generated": false, "language": "Python", "notes": ""}, {"filePath": "test\\function_parameter_error.py", "name": "test.function_parameter_error.py:2", "declaringScopesName": "", "packageName": "test.function_parameter_error", "type": "TOOLERROR", "position": [2, 2], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.function_parameter_error", "id": "591271464", "generated": false, "language": "Python", "notes": "Could not resolve call in file test\\function_parameter_error.py at line 2."}]}'
        self.assertEqual(str(self.result), expected_output)