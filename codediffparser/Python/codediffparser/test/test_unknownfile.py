import unittest
from pathlib import Path

from codediffparser.parser import Parser
from codediffparser.mode import Mode


class TestTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        source_branch = str(Path(__file__).resolve().parent.joinpath('./source/test'))
        target_branch = str(Path(__file__).resolve().parent.joinpath('./target/test'))
        filter_files = ['other.txt']

        parser = Parser()
        parser.parse(target_branch, filter_files, Mode.TARGET)
        parser.parse(source_branch, filter_files, Mode.SOURCE)
        parser.graph.cleanup()
        cls.result = parser.graph


    def test_complete_result_string(self):
        expected_output = r'{"links": [], "nodes": [{"filePath": "other.txt", "name": "other.txt", "declaringScopesName": "", "packageName": "", "type": "UNKNOWNFILE", "position": [], "positionOld": [], "status": "CHANGED", "parentNodeId": null, "id": "other.txt", "generated": false, "language": ""}]}'
        self.assertEqual(str(self.result), expected_output)