import unittest
from pathlib import Path

from codediffparser.parser import Parser
from codediffparser.mode import Mode


class TestTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        source_branch = str(Path(__file__).resolve().parent.joinpath('./source/test'))
        target_branch = str(Path(__file__).resolve().parent.joinpath('./target/test'))
        filter_files = ['simple_class.py']

        parser = Parser()
        parser.parse(target_branch, filter_files, Mode.TARGET)
        parser.parse(source_branch, filter_files, Mode.SOURCE)
        parser.graph.cleanup()
        cls.result = parser.graph
        
    def test_complete_result_string(self):
        expected_output = '{"links": [{"source": "test.simple_mixed.TestClass", "target": "test.simple_mixed.TestClass#__init__3281279809", "relation": "METHOD", "status": "UNCHANGED", "id": "METHOD:test.simple_mixed.TestClass:test.simple_mixed.TestClass#__init__3281279809"}, {"source": "test.simple_mixed.TestClass", "target": "test.simple_mixed.TestClass#test2033572573", "relation": "METHOD", "status": "UNCHANGED", "id": "METHOD:test.simple_mixed.TestClass:test.simple_mixed.TestClass#test2033572573"}, {"source": "test.simple_mixed.TestClass.Inner", "target": "test.simple_mixed.TestClass", "relation": "ENCLOSING_CLASS", "status": "DELETED", "id": "ENCLOSING_CLASS:test.simple_mixed.TestClass.Inner:test.simple_mixed.TestClass"}, {"source": "test.simple_mixed.TestClass.Inner", "target": "test.simple_mixed.TestClass.Inner#inner1539991645", "relation": "METHOD", "status": "DELETED", "id": "METHOD:test.simple_mixed.TestClass.Inner:test.simple_mixed.TestClass.Inner#inner1539991645"}, {"source": "test.simple_mixed.foo3344688307", "target": "test.simple_mixed.foo.bar2607727064", "relation": "FUNCTION", "status": "UNCHANGED", "id": "FUNCTION:test.simple_mixed.foo3344688307:test.simple_mixed.foo.bar2607727064"}, {"source": "test.simple_mixed.foo3344688307", "target": "test.simple_mixed.foo.bar2607727064", "relation": "FUNCTION_CALL", "status": "DELETED", "id": "FUNCTION_CALL:test.simple_mixed.foo3344688307:test.simple_mixed.foo.bar2607727064"}, {"source": "test.simple_mixed.foo_caller2603173153", "target": "test.simple_mixed.foo3344688307", "relation": "FUNCTION_CALL", "status": "UNCHANGED", "id": "FUNCTION_CALL:test.simple_mixed.foo_caller2603173153:test.simple_mixed.foo3344688307"}, {"source": "test.simple_mixed.TestClass", "target": "test.simple_mixed.TestClass#test_caller3618699431", "relation": "METHOD", "status": "ADDED", "id": "METHOD:test.simple_mixed.TestClass:test.simple_mixed.TestClass#test_caller3618699431"}, {"source": "test.simple_mixed.TestClass#test_caller3618699431", "target": "test.simple_mixed.TestClass#test2033572573", "relation": "METHOD_CALL", "status": "ADDED", "id": "METHOD_CALL:test.simple_mixed.TestClass#test_caller3618699431:test.simple_mixed.TestClass#test2033572573"}, {"source": "test.simple_mixed", "target": "test.simple_mixed.TestClass#test_caller3618699431", "relation": "METHOD_CALL", "status": "ADDED", "id": "METHOD_CALL:test.simple_mixed:test.simple_mixed.TestClass#test_caller3618699431"}, {"source": "test.simple_mixed", "target": "test.simple_mixed.foo_caller2603173153", "relation": "FUNCTION_CALL", "status": "ADDED", "id": "FUNCTION_CALL:test.simple_mixed:test.simple_mixed.foo_caller2603173153"}], "nodes": [{"filePath": "test\\simple_mixed.py", "name": "TestClass", "declaringScopesName": "", "packageName": "test.simple_mixed", "type": "CLASS", "position": [1, 11], "positionOld": [1, 10], "status": "CHANGED", "parentNodeId": "test.simple_mixed", "id": "test.simple_mixed.TestClass", "generated": false, "language": "Python"}, {"filePath": "test\\simple_mixed.py", "name": "__init__", "declaringScopesName": "TestClass", "packageName": "test.simple_mixed", "type": "METHOD", "position": [3, 4], "positionOld": [3, 4], "status": "UNCHANGED", "parentNodeId": "test.simple_mixed.TestClass", "id": "test.simple_mixed.TestClass#__init__3281279809", "generated": false, "language": "Python"}, {"filePath": "test\\simple_mixed.py", "name": "test", "declaringScopesName": "TestClass", "packageName": "test.simple_mixed", "type": "METHOD", "position": [6, 7], "positionOld": [6, 7], "status": "UNCHANGED", "parentNodeId": "test.simple_mixed.TestClass", "id": "test.simple_mixed.TestClass#test2033572573", "generated": false, "language": "Python"}, {"filePath": "test\\simple_mixed.py", "name": "Inner", "declaringScopesName": "TestClass", "packageName": "test.simple_mixed", "type": "CLASS", "position": [9, 11], "positionOld": [], "status": "DELETED", "parentNodeId": "test.simple_mixed.TestClass", "id": "test.simple_mixed.TestClass.Inner", "generated": false, "language": "Python"}, {"filePath": "test\\simple_mixed.py", "name": "inner", "declaringScopesName": "TestClass.Inner", "packageName": "test.simple_mixed", "type": "METHOD", "position": [10, 11], "positionOld": [], "status": "DELETED", "parentNodeId": "test.simple_mixed.TestClass.Inner", "id": "test.simple_mixed.TestClass.Inner#inner1539991645", "generated": false, "language": "Python"}, {"filePath": "test\\simple_mixed.py", "name": "foo", "declaringScopesName": "", "packageName": "test.simple_mixed", "type": "FUNCTION", "position": [14, 17], "positionOld": [13, 15], "status": "CHANGED", "parentNodeId": "test.simple_mixed", "id": "test.simple_mixed.foo3344688307", "generated": false, "language": "Python"}, {"filePath": "test\\simple_mixed.py", "name": "bar", "declaringScopesName": "foo", "packageName": "test.simple_mixed", "type": "FUNCTION", "position": [15, 16], "positionOld": [14, 15], "status": "UNCHANGED", "parentNodeId": "test.simple_mixed.foo3344688307", "id": "test.simple_mixed.foo.bar2607727064", "generated": false, "language": "Python"}, {"filePath": "test\\simple_mixed.py", "name": "bar", "declaringScopesName": "foo", "packageName": "test.simple_mixed", "type": "FUNCTION_REFERENCE", "position": [17, 17], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.simple_mixed.foo3344688307", "id": "test.simple_mixed.foo.bar0", "generated": false, "language": "Python"}, {"filePath": "test\\simple_mixed.py", "name": "foo_caller", "declaringScopesName": "", "packageName": "test.simple_mixed", "type": "FUNCTION", "position": [19, 20], "positionOld": [17, 18], "status": "UNCHANGED", "parentNodeId": "test.simple_mixed", "id": "test.simple_mixed.foo_caller2603173153", "generated": false, "language": "Python"}, {"filePath": "test\\simple_mixed.py", "name": "foo", "declaringScopesName": "", "packageName": "test.simple_mixed", "type": "FUNCTION_REFERENCE", "position": [20, 20], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.simple_mixed", "id": "test.simple_mixed.foo0", "generated": false, "language": "Python"}, {"filePath": "test\\simple_mixed.py", "name": "test_caller", "declaringScopesName": "TestClass", "packageName": "test.simple_mixed", "type": "METHOD", "position": [9, 10], "positionOld": [], "status": "ADDED", "parentNodeId": "test.simple_mixed.TestClass", "id": "test.simple_mixed.TestClass#test_caller3618699431", "generated": false, "language": "Python"}, {"filePath": "test\\simple_mixed.py", "name": "test", "declaringScopesName": "TestClass", "packageName": "test.simple_mixed", "type": "METHOD_REFERENCE", "position": [10, 10], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.simple_mixed.TestClass", "id": "test.simple_mixed.TestClass#test0", "generated": false, "language": "Python"}, {"filePath": "test\\simple_mixed.py", "name": "simple_mixed", "declaringScopesName": null, "packageName": "test.simple_mixed", "type": "SCRIPT", "position": [], "positionOld": [], "status": "ADDED", "parentNodeId": null, "id": "test.simple_mixed", "generated": false, "language": "Python"}, {"filePath": "test\\simple_mixed.py", "name": "test_caller", "declaringScopesName": "TestClass", "packageName": "test.simple_mixed", "type": "METHOD_REFERENCE", "position": [22, 22], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.simple_mixed.TestClass", "id": "test.simple_mixed.TestClass#test_caller0", "generated": false, "language": "Python"}, {"filePath": "test\\simple_mixed.py", "name": "foo_caller", "declaringScopesName": "", "packageName": "test.simple_mixed", "type": "FUNCTION_REFERENCE", "position": [24, 24], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.simple_mixed", "id": "test.simple_mixed.foo_caller0", "generated": false, "language": "Python"}]}'
        self.assertTrue(str(self.result), expected_output)