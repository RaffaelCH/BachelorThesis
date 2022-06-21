import ast
import jedi
import re
from os import sep as os_separator
from pathlib import Path
import hashlib

from .graph import Graph
from .node import Node
from .node_type import NodeType
from .status import Status
from .hierarchical_ast_visitor import HierarchicalASTVisitor


class Parser:

    def __init__(self):
        self.graph = Graph()
    

    def get_result(self):
        self.graph.cleanup()
        return str(self.graph)


    def parse(self, sources_root, filter_files, mode):
        separator = "\\\\" if os_separator == "\\" else os_separator
        sources_root = re.sub(r"/|\\", separator, sources_root)
        self.graph.mode = mode

        filter_files_list = [re.sub("\\/|\\\\", separator, file) for file in filter_files]

        for file in filter_files_list:
            if not file.endswith(".py") and not file.endswith(".java"):
                node = Node()
                node.file_path = file
                node.name = file.split(separator)[-1]
                node.type = NodeType.UNKNOWNFILE
                self.graph.add_node(node)
        
        source_paths = []

        for py_file in Path(sources_root).rglob("*.py"):
            if not filter_files_list:
                source_paths.append(py_file)
            elif [f for f in filter_files_list if py_file.parts[-1] == f]:
                source_paths.append(py_file)


        for source_path in source_paths:

            with open(source_path) as source_file:

                try:
                    source = source_file.read()
                except Exception as exception:
                    # Skip this file.
                    # print(f"{64*'!'}\nError {exception=} when reading file {source_path}. Skipping this file.\n{64*'!'}")
                    node = Node()
                    node.file_path = str(source_path)
                    node.name = source_path.name
                    node.type = NodeType.TOOLERROR
                    node.status = Status.CHANGED
                    node.node_hash_code = hashlib.sha256(f"Could not read file {source_path}.".encode('utf-8')).hexdigest()
                    node.notes = f"Could not read file. Reason: {exception=}"
                    self.graph.add_node(node)
                    continue

                try:
                    ast_tree = ast.parse(source)
                except SyntaxError:
                    # Skip this file.
                    # print(f"{64*'!'}\nSyntaxError when parsing file {source_path}. Skipping this file.\n{64*'!'}")
                    node = Node()
                    node.file_path = str(source_path)
                    node.name = source_path.name
                    node.type = NodeType.TOOLERROR
                    node.status = Status.CHANGED
                    node.node_hash_code = hashlib.sha256(f"Could not parse file {source_path}.".encode('utf-8')).hexdigest()
                    node.notes = f"Could not parse file. Reason: {exception=}"
                    self.graph.add_node(node)
                    continue
            
            # TODO: Add progress indicator.
            # print(f"Processing {source_path}.")

            # jedi_project = jedi.get_default_project(source_path)
            jedi_project = jedi.Project(path=sources_root)
            jedi_script = jedi.Script(path=source_path, project=jedi_project)

            visitor = HierarchicalASTVisitor(source, jedi_script, jedi_project, self.graph)
            visitor.visit(ast_tree)
