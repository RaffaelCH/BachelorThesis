import unittest
from pathlib import Path

from codediffparser.parser import Parser
from codediffparser.mode import Mode


class TestTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        source_branch = str(Path(__file__).resolve().parent.joinpath('./source/test'))
        target_branch = str(Path(__file__).resolve().parent.joinpath('./target/test'))
        filter_files = ['nested_class.py']

        parser = Parser()
        parser.parse(target_branch, filter_files, Mode.TARGET)
        parser.parse(source_branch, filter_files, Mode.SOURCE)
        parser.graph.cleanup()
        cls.result = parser.graph


    def test_enclosing_class_link(self):
        try:
            link = self.result.links['ENCLOSING_CLASS:test.nested_class.Outer.Inner:test.nested_class.Outer']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_inner_method_link(self):
        try:
            link = self.result.links['METHOD:test.nested_class.Outer.Inner:test.nested_class.Outer.Inner#inner1539991645']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_outer_method_link(self):
        try:
            link = self.result.links['METHOD:test.nested_class.Outer:test.nested_class.Outer#outer456864278']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_outer_methodcall_link(self):
        try:
            link = self.result.links['METHOD_CALL:test.nested_class:test.nested_class.Outer#outer456864278']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_inner_methodcall_link(self):
        try:
            link = self.result.links['METHOD_CALL:test.nested_class:test.nested_class.Outer.Inner#inner1539991645']
        except KeyError:
            link = None
        self.assertIsNotNone(link)

    
    def test_outer_class_node(self):
        try:
            node = self.result.nodes['test.nested_class.Outer']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_inner_class_node(self):
        try:
            node = self.result.nodes['test.nested_class.Outer.Inner']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_inner_method_node(self):
        try:
            node = self.result.nodes['test.nested_class.Outer.Inner#inner1539991645']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_outer_method_node(self):
        try:
            node = self.result.nodes['test.nested_class.Outer#outer456864278']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_script_node(self):
        try:
            node = self.result.nodes['test.nested_class']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_outer_methodcall_node(self):
        try:
            node = self.result.nodes['test.nested_class.Outer#outer0']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_inner_methodcall_node(self):
        try:
            node = self.result.nodes['test.nested_class.Outer.Inner#inner0']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    
    def test_complete_result_string(self):
        expected_output = r'{"links": [{"source": "test.nested_class.Outer.Inner", "target": "test.nested_class.Outer", "relation": "ENCLOSING_CLASS", "status": "UNCHANGED", "id": "ENCLOSING_CLASS:test.nested_class.Outer.Inner:test.nested_class.Outer"}, {"source": "test.nested_class.Outer.Inner", "target": "test.nested_class.Outer.Inner#inner1539991645", "relation": "METHOD", "status": "UNCHANGED", "id": "METHOD:test.nested_class.Outer.Inner:test.nested_class.Outer.Inner#inner1539991645"}, {"source": "test.nested_class.Outer.Inner#inner1539991645", "target": "builtins.print2978873759", "relation": "FUNCTION_CALL", "status": "UNCHANGED", "id": "FUNCTION_CALL:test.nested_class.Outer.Inner#inner1539991645:builtins.print2978873759"}, {"source": "test.nested_class.Outer", "target": "test.nested_class.Outer#outer456864278", "relation": "METHOD", "status": "UNCHANGED", "id": "METHOD:test.nested_class.Outer:test.nested_class.Outer#outer456864278"}, {"source": "test.nested_class.Outer#outer456864278", "target": "builtins.print2978873759", "relation": "FUNCTION_CALL", "status": "UNCHANGED", "id": "FUNCTION_CALL:test.nested_class.Outer#outer456864278:builtins.print2978873759"}, {"source": "test.nested_class", "target": "test.nested_class.Outer#outer456864278", "relation": "METHOD_CALL", "status": "UNCHANGED", "id": "METHOD_CALL:test.nested_class:test.nested_class.Outer#outer456864278"}, {"source": "test.nested_class", "target": "test.nested_class.Outer.Inner#inner1539991645", "relation": "METHOD_CALL", "status": "UNCHANGED", "id": "METHOD_CALL:test.nested_class:test.nested_class.Outer.Inner#inner1539991645"}], "nodes": [{"filePath": "test\\nested_class.py", "name": "Outer", "declaringScopesName": "", "packageName": "test.nested_class", "type": "CLASS", "position": [1, 8], "positionOld": [1, 8], "status": "UNCHANGED", "parentNodeId": "test.nested_class", "id": "test.nested_class.Outer", "generated": false, "language": "Python"}, {"filePath": "test\\nested_class.py", "name": "Inner", "declaringScopesName": "Outer", "packageName": "test.nested_class", "type": "CLASS", "position": [3, 5], "positionOld": [3, 5], "status": "UNCHANGED", "parentNodeId": "test.nested_class.Outer", "id": "test.nested_class.Outer.Inner", "generated": false, "language": "Python"}, {"filePath": "test\\nested_class.py", "name": "inner", "declaringScopesName": "Outer.Inner", "packageName": "test.nested_class", "type": "METHOD", "position": [4, 5], "positionOld": [4, 5], "status": "UNCHANGED", "parentNodeId": "test.nested_class.Outer.Inner", "id": "test.nested_class.Outer.Inner#inner1539991645", "generated": false, "language": "Python"}, {"filePath": null, "name": "print", "declaringScopesName": "", "packageName": "builtins", "type": "FUNCTION_REFERENCE", "position": [5, 5], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "builtins", "id": "builtins.print2706448491", "generated": false, "language": "Python"}, {"filePath": "test\\nested_class.py", "name": "outer", "declaringScopesName": "Outer", "packageName": "test.nested_class", "type": "METHOD", "position": [7, 8], "positionOld": [7, 8], "status": "UNCHANGED", "parentNodeId": "test.nested_class.Outer", "id": "test.nested_class.Outer#outer456864278", "generated": false, "language": "Python"}, {"filePath": null, "name": "print", "declaringScopesName": "", "packageName": "builtins", "type": "FUNCTION_REFERENCE", "position": [8, 8], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "builtins", "id": "builtins.print1988473640", "generated": false, "language": "Python"}, {"filePath": "test\\nested_class.py", "name": "nested_class", "declaringScopesName": null, "packageName": "test.nested_class", "type": "SCRIPT", "position": [], "positionOld": [], "status": "DELETED", "parentNodeId": null, "id": "test.nested_class", "generated": false, "language": "Python"}, {"filePath": "test\\nested_class.py", "name": "outer", "declaringScopesName": "Outer", "packageName": "test.nested_class", "type": "METHOD_REFERENCE", "position": [12, 12], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.nested_class.Outer", "id": "test.nested_class.Outer#outer0", "generated": false, "language": "Python"}, {"filePath": "test\\nested_class.py", "name": "inner", "declaringScopesName": "Outer.Inner", "packageName": "test.nested_class", "type": "METHOD_REFERENCE", "position": [15, 15], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.nested_class.Outer.Inner", "id": "test.nested_class.Outer.Inner#inner0", "generated": false, "language": "Python"}]}'
        self.assertEqual(str(self.result), expected_output)