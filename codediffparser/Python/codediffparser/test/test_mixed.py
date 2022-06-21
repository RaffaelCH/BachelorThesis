import unittest
from pathlib import Path

from codediffparser.parser import Parser
from codediffparser.mode import Mode


class TestTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        source_branch = str(Path(__file__).resolve().parent.joinpath('./source/test'))
        target_branch = str(Path(__file__).resolve().parent.joinpath('./target/test'))
        filter_files = ['mixed.py']

        parser = Parser()
        parser.parse(target_branch, filter_files, Mode.TARGET)
        parser.parse(source_branch, filter_files, Mode.SOURCE)
        parser.graph.cleanup()
        cls.result = parser.graph


    def test_superclass_link(self):
        try:
            link = self.result.links['SUPERCLASS:test.mixed.Sub:test.nested_class.Outer.Inner']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_sub_init_method_link(self):
        try:
            link = self.result.links['METHOD:test.mixed.Sub:test.mixed.Sub#__init__3281279809']
        except KeyError:
            link = None
        self.assertIsNotNone(link)

    def test_sub_init_methodcall_link(self):
        try:
            link = self.result.links['METHOD_CALL:test.mixed.Sub#__init__3281279809:test.nested_class.Outer.Inner#inner1539991645']
        except KeyError:
            link = None
        self.assertIsNotNone(link)

    def test_inner_method_link(self):
        try:
            link = self.result.links['METHOD:test.nested_class.Outer.Inner:test.nested_class.Outer.Inner#inner1539991645']
        except KeyError:
            link = None
        self.assertIsNotNone(link)

    def test_subclass_method_link(self):
        try:
            link = self.result.links['METHOD:test.mixed.Sub:test.mixed.Sub#foo_caller2859335271']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_functioncall_from_method_link(self):
        try:
            link = self.result.links['FUNCTION_CALL:test.mixed.Sub#foo_caller2859335271:test.simple_function.foo3539003634']
        except KeyError:
            link = None
        self.assertIsNotNone(link)

    def test_static_method_link(self):
        try:
            link = self.result.links['METHOD:test.mixed.Sub:test.mixed.Sub#static2416854815']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_builtin_functioncall_link(self):
        try:
            link = self.result.links['FUNCTION_CALL:test.mixed.Sub#static2416854815:builtins.print2978873759']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_methodcall_link(self):
        try:
            link = self.result.links['METHOD_CALL:test.mixed:test.mixed.Sub#foo_caller2859335271']
        except KeyError:
            link = None
        self.assertIsNotNone(link)
    
    def test_static_methodcall_link(self):
        try:
            link = self.result.links['METHOD_CALL:test.mixed:test.mixed.Sub#static2416854815']
        except KeyError:
            link = None
        self.assertIsNotNone(link)

    
    def test_inner_class_node(self):
        try:
            node = self.result.nodes['test.nested_class.Outer.Inner']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_subclass_node(self):
        try:
            node = self.result.nodes['test.mixed.Sub']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_subclass_init_node(self):
        try:
            node = self.result.nodes['test.mixed.Sub#__init__3281279809']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_inner_method_node(self):
        try:
            node = self.result.nodes['test.nested_class.Outer.Inner#inner0']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_method_node(self):
        try:
            node = self.result.nodes['test.mixed.Sub#foo_caller2859335271']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
        
    def test_function_node(self):
        try:
            node = self.result.nodes['test.simple_function.foo3303759665']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
        
    def test_static_method_node(self):
        try:
            node = self.result.nodes['test.mixed.Sub#static2416854815']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
        
    def test_builtins_node(self):
        try:
            node = self.result.nodes['builtins.print2102509221']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_script_node(self):
        try:
            node = self.result.nodes['test.mixed.Sub#foo_caller0']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
    
    def test_script_node(self):
        try:
            node = self.result.nodes['test.mixed']
        except KeyError:
            node = None
        self.assertIsNotNone(node)

    def test_script_node(self):
        try:
            node = self.result.nodes['test.mixed.Sub#static0']
        except KeyError:
            node = None
        self.assertIsNotNone(node)
        
    
    def test_complete_result_string(self):
        expected_output = r'{"links": [{"source": "test.mixed.Sub", "target": "test.nested_class.Outer.Inner", "relation": "SUPERCLASS", "status": "UNCHANGED", "id": "SUPERCLASS:test.mixed.Sub:test.nested_class.Outer.Inner"}, {"source": "test.mixed.Sub", "target": "test.mixed.Sub#__init__3281279809", "relation": "METHOD", "status": "UNCHANGED", "id": "METHOD:test.mixed.Sub:test.mixed.Sub#__init__3281279809"}, {"source": "test.mixed.Sub#__init__3281279809", "target": "test.nested_class.Outer.Inner#inner1539991645", "relation": "METHOD_CALL", "status": "UNCHANGED", "id": "METHOD_CALL:test.mixed.Sub#__init__3281279809:test.nested_class.Outer.Inner#inner1539991645"}, {"source": "test.nested_class.Outer.Inner", "target": "test.nested_class.Outer.Inner#inner1539991645", "relation": "METHOD", "status": "UNCHANGED", "id": "METHOD:test.nested_class.Outer.Inner:test.nested_class.Outer.Inner#inner1539991645"}, {"source": "test.mixed.Sub", "target": "test.mixed.Sub#foo_caller2859335271", "relation": "METHOD", "status": "UNCHANGED", "id": "METHOD:test.mixed.Sub:test.mixed.Sub#foo_caller2859335271"}, {"source": "test.mixed.Sub#foo_caller2859335271", "target": "test.simple_function.foo3539003634", "relation": "FUNCTION_CALL", "status": "UNCHANGED", "id": "FUNCTION_CALL:test.mixed.Sub#foo_caller2859335271:test.simple_function.foo3539003634"}, {"source": "test.mixed.Sub", "target": "test.mixed.Sub#static2416854815", "relation": "METHOD", "status": "UNCHANGED", "id": "METHOD:test.mixed.Sub:test.mixed.Sub#static2416854815"}, {"source": "test.mixed.Sub#static2416854815", "target": "builtins.print2978873759", "relation": "FUNCTION_CALL", "status": "UNCHANGED", "id": "FUNCTION_CALL:test.mixed.Sub#static2416854815:builtins.print2978873759"}, {"source": "test.mixed", "target": "test.mixed.Sub#foo_caller2859335271", "relation": "METHOD_CALL", "status": "UNCHANGED", "id": "METHOD_CALL:test.mixed:test.mixed.Sub#foo_caller2859335271"}, {"source": "test.mixed", "target": "test.mixed.Sub#static2416854815", "relation": "METHOD_CALL", "status": "UNCHANGED", "id": "METHOD_CALL:test.mixed:test.mixed.Sub#static2416854815"}], "nodes": [{"filePath": "test\\nested_class.py", "name": "Inner", "declaringScopesName": "Outer", "packageName": "test.nested_class", "type": "TYPE_REFERENCE", "position": [3, 5], "positionOld": [], "status": "UNCHANGED", "parentNodeId": null, "id": "test.nested_class.Outer.Inner", "generated": false, "language": "Python", "notes": ""}, {"filePath": "test\\mixed.py", "name": "Sub", "declaringScopesName": "", "packageName": "test.mixed", "type": "CLASS", "position": [5, 14], "positionOld": [5, 14], "status": "UNCHANGED", "parentNodeId": "test.mixed", "id": "test.mixed.Sub", "generated": false, "language": "Python", "notes": ""}, {"filePath": "test\\mixed.py", "name": "__init__", "declaringScopesName": "Sub", "packageName": "test.mixed", "type": "METHOD", "position": [7, 8], "positionOld": [7, 8], "status": "UNCHANGED", "parentNodeId": "test.mixed.Sub", "id": "test.mixed.Sub#__init__3281279809", "generated": false, "language": "Python", "notes": ""}, {"filePath": "test\\nested_class.py", "name": "inner", "declaringScopesName": "Outer.Inner", "packageName": "test.nested_class", "type": "METHOD_REFERENCE", "position": [8, 8], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.nested_class.Outer.Inner", "id": "test.nested_class.Outer.Inner#inner0", "generated": false, "language": "Python", "notes": ""}, {"filePath": "test\\mixed.py", "name": "foo_caller", "declaringScopesName": "Sub", "packageName": "test.mixed", "type": "METHOD", "position": [10, 11], "positionOld": [10, 11], "status": "UNCHANGED", "parentNodeId": "test.mixed.Sub", "id": "test.mixed.Sub#foo_caller2859335271", "generated": false, "language": "Python", "notes": ""}, {"filePath": "test\\simple_function.py", "name": "foo", "declaringScopesName": "", "packageName": "test.simple_function", "type": "FUNCTION_REFERENCE", "position": [11, 11], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.simple_function", "id": "test.simple_function.foo3303759665", "generated": false, "language": "Python", "notes": ""}, {"filePath": "test\\mixed.py", "name": "static", "declaringScopesName": "Sub", "packageName": "test.mixed", "type": "METHOD", "position": [13, 14], "positionOld": [13, 14], "status": "UNCHANGED", "parentNodeId": "test.mixed.Sub", "id": "test.mixed.Sub#static2416854815", "generated": false, "language": "Python", "notes": ""}, {"filePath": null, "name": "print", "declaringScopesName": "", "packageName": "builtins", "type": "FUNCTION_REFERENCE", "position": [14, 14], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "builtins", "id": "builtins.print2102509221", "generated": false, "language": "Python", "notes": ""}, {"filePath": "test\\mixed.py", "name": "foo_caller", "declaringScopesName": "Sub", "packageName": "test.mixed", "type": "METHOD_REFERENCE", "position": [17, 17], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.mixed.Sub", "id": "test.mixed.Sub#foo_caller0", "generated": false, "language": "Python", "notes": ""}, {"filePath": "test\\mixed.py", "name": "mixed", "declaringScopesName": null, "packageName": "test.mixed", "type": "SCRIPT", "position": [], "positionOld": [], "status": "UNCHANGED", "parentNodeId": null, "id": "test.mixed", "generated": false, "language": "Python", "notes": ""}, {"filePath": "test\\mixed.py", "name": "static", "declaringScopesName": "Sub", "packageName": "test.mixed", "type": "METHOD_REFERENCE", "position": [18, 18], "positionOld": [], "status": "UNCHANGED", "parentNodeId": "test.mixed.Sub", "id": "test.mixed.Sub#static0", "generated": false, "language": "Python", "notes": ""}]}'
        self.assertEqual(str(self.result), expected_output)