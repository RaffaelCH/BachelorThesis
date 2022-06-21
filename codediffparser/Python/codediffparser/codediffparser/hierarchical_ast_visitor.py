import ast
import re

#from .graph import Graph
from .node import Node, NodeType
from .node_type import NodeType
from .link import Link
from .link_relation import LinkRelation
from .qualified_name_helper import QualifiedNameHelper


# Hierarchically visits all ast nodes.
# Extracts the entities of interest and adds them (together with their relation) to the graph.
class HierarchicalASTVisitor(ast.NodeVisitor):

    def __init__(self, source_code, jedi_script, jedi_project, graph):
        self._source = source_code
        self._jedi_script = jedi_script
        self._jedi_project = jedi_project
        self.graph = graph
    

    def _get_project_name(self):
        return self._jedi_project.path.parts[-1]

    def _get_script_qualifier(self):
        """Returns the qualifier of the current jedi script in the form 'subdir1.subdir2.filename'."""
        rel_path = self._jedi_script.path.relative_to(self._jedi_project.path)
        rel_str = ".".join(rel_path.parts)
        rel_str = rel_str[:-len(rel_path.suffix)]
        return rel_str
        

    def _annotate_ast_children(self, ast_node):
        """Add Attribute to each childnode linking to the node defining the enclosing scope (function/class)."""
        for node in ast.walk(ast_node):
            node.enclosing_scope_node = ast_node
    
    def _get_enclosing_scope_node(self, ast_node):
        """If child of function/class node, return this node."""
        try:
            return ast_node.enclosing_scope_node
        except AttributeError:
            return None
    

    def _get_relative_file_path(self, jedi_node):
        """Get filepath relative to the project root."""
        if jedi_node.module_path and jedi_node.module_path.is_relative_to(self._jedi_project.path):
            return str(jedi_node.module_path.relative_to(self._jedi_project.path))
        return None


    def _get_call_jedi_position(self, node):
        """Return the position in the file for an ast.Call node."""
        
        if type(node) is not ast.Call:
            return

        source_code = ast.get_source_segment(self._source, node.func)

        if type(node.func) is ast.Attribute:
            start_index = source_code.rfind(node.func.attr)
        elif type(node.func) is ast.Name:
            start_index = source_code.find(node.func.id)
        else:
            start_index = 0 # TODO
        
        # compute the actual position in the file
        splitted = source_code[:start_index].splitlines() if len(source_code[:start_index]) > 0 else [' ']
        lines_offset = len(splitted) - 1
        columns_offset = len(splitted[-1])

        if lines_offset > 0:
            return (node.lineno + lines_offset, columns_offset)
        return (node.lineno + lines_offset, node.col_offset + columns_offset)


    def _get_def_name_jedi_position(self, ast_node):
        """Returns the original position of the name for a definition as (line, column)."""
        source_code = ast.get_source_segment(self._source, ast_node)
        if type(ast_node) is ast.ClassDef:
            start_index = re.search('class[\\\\\s]*', source_code).end()
        elif type(ast_node) is ast.FunctionDef:
            start_index = re.search('def[\\\\\s]*', source_code).end()
        elif type(ast_node) is ast.AsyncFunctionDef:
            start_index = re.search('async[\\\\\s]*def[\\\\\s]*', source_code).end()
        else:
            # print("Error: Could not get definition position.")
            return (0, 0) # Throw error?
        
        # compute the actual position in the file
        splitted = source_code[:start_index].splitlines()
        lines_offset = len(splitted) - 1
        columns_offset = len(splitted[-1])
        # TODO: check string at position == node.name

        return (ast_node.lineno + lines_offset, ast_node.col_offset + columns_offset)
    

    def _get_jedi_module_name(self, jedi_node):
        """Return the name of the jedi module (file) relative to the project."""
        if jedi_node.module_path and self._jedi_project.path in jedi_node.module_path.parents:
            relative_path = jedi_node.module_path.relative_to(self._jedi_project.path)
            project_name = ".".join(relative_path.parts)[:-len(relative_path.suffix)]
            return project_name
        else:
            return jedi_node.full_name


    def _get_jedi_full_name(self, jedi_node):
        """Return the full name of a jedi node (relative to the project if possible)."""
        if not jedi_node:
            return "" # Error?
        elif not jedi_node.module_path:
            return jedi_node.full_name
        # Import from different file?
        elif jedi_node.module_path != self._jedi_script.path:
            # Import from same project?
            if self._jedi_project.path in jedi_node.module_path.parents:
                relative_path = jedi_node.module_path.relative_to(self._jedi_project.path)
                relative_name = ".".join(relative_path.parts[:-1])
                relative_name += f".{jedi_node.full_name}"
                return relative_name
            else:
                return jedi_node.full_name
        elif jedi_node.is_definition() and jedi_node.full_name:
            return jedi_node.full_name
        return self._get_jedi_full_name(jedi_node.parent()) + "." + jedi_node.name


    def _concat_declaring_names(self, jedi_node):
        """Concatenates class and function names enclosing the jedi node."""
        classes_names = []
        while jedi_node.parent() and jedi_node.parent().type != 'module':
            classes_names.append(jedi_node.parent().name)
            jedi_node = jedi_node.parent()
        classes_names.reverse()
        return QualifiedNameHelper.concat_save(*classes_names)
    
    
    def _hash_string(self, string):
        my_hash = 0
        for char in string:
            my_hash = (my_hash*281 ^ ord(char)*997) & 0xFFFFFFFF
        return my_hash

    def _hash_call_args(self, call_node):
        """Hashes the arguments for an ast.Call node."""
        hashed = ""
        for arg in call_node.args:
            hashed += ast.dump(arg)
        return self._hash_string(hashed)
    
    def _hash_jedi_linecode(self, jedi_node):
        try:
            linecode = jedi_node.get_line_code()
        except TypeError:
            return 0
        return self._hash_string(linecode)
    
    
    def _get_signature_string(self, jedi_node):
        """Get the signature of a function if it exists and hash it."""
        signatures = jedi_node.get_signatures()
        if len(signatures) > 0:
            return str(self._hash_string(signatures[0].to_string()))
        else:
            return "0"
    

    def _add_error_node(self, message, lineno):
        """Add an error node connected to the current script node with the message in the notes."""

        rel_filepath = self._jedi_script.path.relative_to(self._jedi_project.path)
        project_name = ".".join(rel_filepath.parts)[:-len(self._jedi_script.path.suffix)]

        # Add script node for the file in which error originates.
        script_node = Node()
        script_node.file_path = str(rel_filepath)
        script_node.name = self._jedi_script.path.name[:-len(self._jedi_script.path.suffix)]
        script_node.declaring_classes_name = None
        script_node.project_name = project_name
        script_node.type = NodeType.SCRIPT
        script_node.parent_node_id = None
        self.graph.add_node(script_node)

        # Add error node for the error.
        error_node = Node()
        error_node.file_path = str(rel_filepath)
        error_node.name =  ".".join(rel_filepath.parts) + ":" + str(lineno)
        error_node.declaring_classes_name = ""
        error_node.project_name = project_name
        error_node.type = NodeType.TOOLERROR
        error_node.position = [lineno, lineno]
        error_node.parent_node_id = project_name
        error_node.node_hash_code = self._hash_string(message + str(lineno))
        error_node.is_generated = False
        error_node.notes = message
        self.graph.add_node(error_node)

        error_link = Link()
        error_link.source = project_name
        error_link.target = error_node.get_id()
        error_link.relation = LinkRelation.TOOLERROR
        self.graph.add_link(error_link)



    def visit_FunctionDef(self, node):
        """NodeVisitor.ast method: add nodes, links for a function definition to the graph."""

        position = self._get_def_name_jedi_position(node)
        jedi_nodes = self._jedi_script.infer(*position)

        if len(jedi_nodes) == 0:
            self._add_error_node(f"Could not resolve function definition in file {self._jedi_script.path.relative_to(self._jedi_project.path)} at line {node.lineno}.", node.lineno)
            self.generic_visit(node)
            return

        jedi_node = jedi_nodes[0]
        jedi_parent = jedi_node.parent()

        source = QualifiedNameHelper.concat_save(*self._get_jedi_full_name(jedi_parent).split("."))

        # Method definition.
        if (jedi_node.parent().type == 'class'):
            method_node = Node()
            method_node.file_path = self._get_relative_file_path(jedi_node)
            method_node.name = node.name
            method_node.declaring_classes_name = self._concat_declaring_names(jedi_node)
            method_node.project_name = self._get_jedi_module_name(jedi_node)
            method_node.type = NodeType.METHOD
            method_node.position = [jedi_node.get_definition_start_position()[0], jedi_node.get_definition_end_position()[0]]
            method_node.parent_node_id = source
            method_node.node_hash_code = self._hash_string(ast.dump(node))
            method_node.param_hash_code = self._hash_jedi_linecode(jedi_node)
            method_node.is_generated = False
            self.graph.add_node(method_node)

            method_link = Link()
            method_link.source = source
            method_link.target = QualifiedNameHelper.concat_save_with_delimiter("#", source, node.name)  + str(self._hash_jedi_linecode(jedi_node))
            method_link.relation = LinkRelation.METHOD
            self.graph.add_link(method_link)

        # Nested function definition.
        elif (jedi_parent.type == 'function'):
            function_node = Node()
            function_node.file_path = self._get_relative_file_path(jedi_node)
            function_node.name = node.name
            function_node.declaring_classes_name = self._concat_declaring_names(jedi_node)
            function_node.project_name = self._get_jedi_module_name(jedi_node)
            function_node.type = NodeType.FUNCTION
            function_node.position = [jedi_node.get_definition_start_position()[0], jedi_node.get_definition_end_position()[0]]
            function_node.parent_node_id = source + self._get_signature_string(jedi_parent)
            function_node.node_hash_code = self._hash_string(ast.dump(node))
            function_node.param_hash_code = self._get_signature_string(jedi_node)
            function_node.is_generated = False
            self.graph.add_node(function_node)

            function_link = Link()
            function_link.source = QualifiedNameHelper.concat_save(source, node.name) + self._get_signature_string(jedi_node)
            function_link.target = source + self._get_signature_string(jedi_parent)
            function_link.relation = LinkRelation.FUNCTION
            self.graph.add_link(function_link)
        
        # Top-level function definition.
        else:
            function_node = Node()
            function_node.file_path = self._get_relative_file_path(jedi_node)
            function_node.name = node.name
            function_node.declaring_classes_name = self._concat_declaring_names(jedi_node)
            function_node.project_name = self._get_jedi_module_name(jedi_node)
            function_node.type = NodeType.FUNCTION
            function_node.position = [jedi_node.get_definition_start_position()[0], jedi_node.get_definition_end_position()[0]]
            function_node.parent_node_id = None
            function_node.node_hash_code = self._hash_string(ast.dump(node))
            function_node.param_hash_code = self._get_signature_string(jedi_node)
            function_node.is_generated = False
            self.graph.add_node(function_node)

        self._annotate_ast_children(node)
        self.generic_visit(node)
    
    
    def visit_AsyncFunctionDef(self, node):
        self.visit_ClassDef(node)


    # Class definition, name is class name, bases is list of nodes for explicitly specified base classes,
    # body is body, decorator_list is list of nodes.
    def visit_ClassDef(self, node):
        """NodeVisitor.ast method: add nodes, links for a class definition to the graph."""

        position = self._get_def_name_jedi_position(node) # TODO: Add error handling/checking.
        jedi_nodes = self._jedi_script.infer(*position)

        if len(jedi_nodes) == 0:
            self._add_error_node(f"Could not resolve class definition in file {self._jedi_script.path.relative_to(self._jedi_project.path)} at line {node.lineno}.", node.lineno)
            self.generic_visit(node)
            return

        jedi_node = jedi_nodes[0]
        full_name = self._get_jedi_full_name(jedi_node)
        source = QualifiedNameHelper.concat_save(*full_name.split("."))

        # Add superclasses (if present).
        for base_node in node.bases:
            superclasses = self._jedi_script.infer(base_node.end_lineno, base_node.end_col_offset)

            if len(superclasses) == 0:
                self._add_error_node(f"Could not resolve superclass definition in file {self._jedi_script.path.relative_to(self._jedi_project.path)} at line {node.lineno}.", node.lineno)
                self.generic_visit(node)
                return

            superclass = superclasses[0]
            
            # Superclass
            super_node = Node()
            super_node.file_path = self._get_relative_file_path(superclass)
            super_node.name = superclass.name
            super_node.declaring_classes_name = self._concat_declaring_names(superclass)
            super_node.project_name = self._get_jedi_module_name(superclass)
            super_node.type = NodeType.TYPE_REFERENCE
            super_node.position = [superclass.get_definition_start_position()[0], superclass.get_definition_end_position()[0]]
            super_node.parent_node_id = None # Add?
            # TODO: Add decorators as modifiers?
            self.graph.add_node(super_node)

            super_link = Link()
            super_link.source = source
            super_link.target = self._get_jedi_full_name(superclass)
            super_link.relation = LinkRelation.SUPERCLASS
            self.graph.add_link(super_link)

        # Add class node.
        class_node = Node()
        class_node.file_path = self._get_relative_file_path(jedi_node)
        class_node.name = node.name
        class_node.declaring_classes_name = self._concat_declaring_names(jedi_node)
        class_node.project_name = self._get_jedi_module_name(jedi_node)
        class_node.type = NodeType.CLASS
        class_node.position = [node.lineno, node.end_lineno]
        class_node.parent_node_id = self._get_jedi_full_name(jedi_node.parent()) + (self._get_signature_string(jedi_node) if jedi_node.parent().type == 'function' else "")
        class_node.node_hash_code = self._hash_string(ast.dump(node))
        self.graph.add_node(class_node)

        # Nested in another class.
        if jedi_node.parent().type == 'class':
            enclosing_link = Link()
            enclosing_link.source = source
            enclosing_link.target = self._get_jedi_full_name(jedi_node.parent())
            enclosing_link.relation = LinkRelation.ENCLOSING_CLASS
            self.graph.add_link(enclosing_link)

        # Nested in a function.
        elif jedi_node.parent().type == 'function':
            enclosing_link = Link()
            enclosing_link.source = source + self._get_signature_string(jedi_node.parent())
            enclosing_link.target = self._get_jedi_full_name(jedi_node.parent()) + self._get_signature_string(jedi_node.parent())
            enclosing_link.relation = LinkRelation.FUNCTION
            self.graph.add_link(enclosing_link)

        self._annotate_ast_children(node)
        self.generic_visit(node)
    

    def visit_Call(self, node):
        """NodeVisitor.ast method: add nodes, links for a function/method call to the graph."""

        position = self._get_call_jedi_position(node) # TODO: Add error handling/checking.
        jedi_nodes = self._jedi_script.infer(*position)

        if len(jedi_nodes) == 0:
            self._add_error_node(f"Could not resolve call in file {self._jedi_script.path.relative_to(self._jedi_project.path)} at line {node.lineno}.", node.lineno)
            self.generic_visit(node)
            return
        
        jedi_node = jedi_nodes[0]

        try:
            jedi_parent = jedi_node.parent() # target parent
        except:
            jedi_parent = None

        if not jedi_parent:
            self._add_error_node(f"Could not get parent of {jedi_node.name} in file {self._jedi_script.path.relative_to(self._jedi_project.path)} at line {node.lineno}.", node.lineno)
            self.generic_visit(node)
            return

        jedi_parent_full_name = self._get_jedi_full_name(jedi_parent)
        parent_node_id = jedi_parent_full_name + (self._get_signature_string(jedi_node.parent()) if jedi_node.parent().type == 'function' else "")
        declaring_project = self._get_jedi_module_name(jedi_parent)

        qualified_method_name_target = QualifiedNameHelper.concat_save_with_delimiter("#", jedi_parent_full_name, jedi_node.name) + str(self._hash_jedi_linecode(jedi_node))
        qualified_function_name_target = QualifiedNameHelper.concat_save(jedi_parent_full_name, jedi_node.name) + self._get_signature_string(jedi_node)

        enclosing_node = self._get_enclosing_scope_node(node)

        if enclosing_node:
            position = self._get_def_name_jedi_position(enclosing_node)
            enclosing_jedi_node = self._jedi_script.infer(*position)[0]
            parent_source = self._get_jedi_full_name(enclosing_jedi_node.parent())

            if enclosing_jedi_node.parent().type == 'class':
                source = QualifiedNameHelper.concat_save_with_delimiter("#", parent_source, enclosing_jedi_node.name) + str(self._hash_jedi_linecode(enclosing_jedi_node))
            else:
                source = QualifiedNameHelper.concat_save(parent_source, enclosing_jedi_node.name) + self._get_signature_string(enclosing_jedi_node)
        else:
            source = self._get_script_qualifier() # Call originates in script (not in any code entity).

        # Special case of constructor (__init__).
        if jedi_node.type == 'class':
            # TYPE relation?
            pass # TODO
        
        # Method call
        elif jedi_parent.type == 'class':

            # Add reference to class node for this method.
            type_reference_node = Node()
            type_reference_node.file_path = self._get_relative_file_path(jedi_node)
            type_reference_node.name = jedi_parent.name
            type_reference_node.declaring_classes_name = self._concat_declaring_names(jedi_parent)
            type_reference_node.project_name = declaring_project
            type_reference_node.type = NodeType.TYPE_REFERENCE
            type_reference_node.position = [node.lineno, node.end_lineno]
            type_reference_node.parent_node_id = self._get_jedi_full_name(jedi_parent.parent())
            self.graph.add_node(type_reference_node)

            # Add reference to method node itself.
            method_reference_node = Node()
            method_reference_node.file_path = self._get_relative_file_path(jedi_node)
            method_reference_node.name = jedi_node.name
            method_reference_node.declaring_classes_name = self._concat_declaring_names(jedi_node)
            method_reference_node.project_name = declaring_project
            method_reference_node.type = NodeType.METHOD_REFERENCE
            method_reference_node.position = [node.lineno, node.end_lineno]
            method_reference_node.parent_node_id = parent_node_id
            method_reference_node.param_hash_code = self._hash_call_args(node)
            self.graph.add_node(method_reference_node)

            # Add link from calling node to method.
            method_call_link = Link()
            method_call_link.source = source
            method_call_link.target = qualified_method_name_target
            method_call_link.relation = LinkRelation.METHOD_CALL
            self.graph.add_link(method_call_link)

            # Add link from method to class node.
            method_link = Link()
            method_link.source = parent_node_id
            method_link.target = qualified_method_name_target
            method_link.relation = LinkRelation.METHOD
            self.graph.add_link(method_link)

        # Function call.
        else:
            function_reference_node = Node()
            function_reference_node.file_path = self._get_relative_file_path(jedi_node)
            function_reference_node.name = jedi_node.name
            function_reference_node.declaring_classes_name = self._concat_declaring_names(jedi_node)
            function_reference_node.project_name = declaring_project
            function_reference_node.type = NodeType.FUNCTION_REFERENCE
            function_reference_node.position = [node.lineno, node.end_lineno]
            function_reference_node.parent_node_id = parent_node_id
            function_reference_node.param_hash_code = self._hash_call_args(node)
            self.graph.add_node(function_reference_node)

            function_link = Link()
            function_link.source = source
            function_link.target = qualified_function_name_target
            function_link.relation = LinkRelation.FUNCTION_CALL
            self.graph.add_link(function_link)
        
        # Reference originates from script (not in class/function).
        if not enclosing_node:
            rel_filepath = self._jedi_script.path.relative_to(self._jedi_project.path)
            filename = self._jedi_script.path.name[:-len(self._jedi_script.path.suffix)]

            script_node = Node()
            script_node.file_path = str(rel_filepath)
            script_node.name = filename
            script_node.declaring_classes_name = None
            script_node.project_name = ".".join(rel_filepath.parts)[:-len(self._jedi_script.path.suffix)]
            script_node.type = NodeType.SCRIPT
            script_node.parent_node_id = None
            self.graph.add_node(script_node)

        self.generic_visit(node)