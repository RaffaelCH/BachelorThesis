import unittest
from pathlib import Path

from codediffparser.parser import Parser
from codediffparser.mode import Mode


class TestTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        source_branch = str(Path(__file__).resolve().parent.joinpath('./source/test'))
        target_branch = str(Path(__file__).resolve().parent.joinpath('./target/test'))
        filter_files = ['builtins.py']

        parser = Parser()
        parser.parse(target_branch, filter_files, Mode.TARGET)
        parser.parse(source_branch, filter_files, Mode.SOURCE)
        parser.graph.cleanup()
        cls.result = parser.graph


    def test_import_link(self):
        try:
            link = self.result.links['FUNCTION_CALL:test.builtins:math.sin1678916783']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_global_namespace_link(self):
        try:
            link = self.result.links['FUNCTION_CALL:test.builtins:builtins.print2978873759']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    

    def test_import_function_node(self):
        try:
            node = self.result.nodes['math.sin3224600221']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_builtins_function_node(self):
        try:
            node = self.result.nodes['test.builtins']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_builtins_node(self):
        try:
            node = self.result.nodes['builtins.print576527066']
        except KeyError:
            node = None
        self.assertIsNotNone(node)

    
    def test_complete_result_string(self):
        expected_output = r'{"links": [{"source": "test.builtins", "target": "math.sin1678916783", "relation": "FUNCTION_CALL", "status": "UNCHANGED", "id": "FUNCTION_CALL:test.builtins:math.sin1678916783"}, {"source": "test.builtins", "target": "builtins.print2978873759", "relation": "FUNCTION_CALL", "status": "UNCHANGED", "id": "FUNCTION_CALL:test.builtins:builtins.print2978873759"}], "nodes": [{"filePath": null, "name": "sin", "declaringScopesName": "", "packageName": "math", "type": "FUNCTION_REFERENCE", "position": [4, 4], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "math", "id": "math.sin3224600221", "generated": false, "language": "Python", "notes": ""}, {"filePath": "test\\builtins.py", "name": "builtins", "declaringScopesName": null, "packageName": "test.builtins", "type": "SCRIPT", "position": [], "positionOld": [], "status": "UNCHANGED", "parentNodeId": null, "id": "test.builtins", "generated": false, "language": "Python", "notes": ""}, {"filePath": null, "name": "print", "declaringScopesName": "", "packageName": "builtins", "type": "FUNCTION_REFERENCE", "position": [7, 7], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "builtins", "id": "builtins.print576527066", "generated": false, "language": "Python", "notes": ""}]}'
        self.assertEqual(str(self.result), expected_output)