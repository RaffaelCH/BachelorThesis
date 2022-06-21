import json

from .mode import Mode
from .status import Status


class Graph():

    def __init__(self):
        self.links = {}
        self.nodes = {}
        self.mode = Mode.TARGET
    

    def _status_new(self):
        if self.mode is Mode.TARGET:
            return Status.DELETED
        return Status.ADDED
    

    def _update_status(self, link):
        if link.status is not Status.ADDED and link.status is not self._status_new():
            link.status = Status.UNCHANGED
    

    def add_link(self, link):
        try:
            graph_link = self.links[link.get_id()]
            self._update_status(graph_link)
        except KeyError:
            link.status = self._status_new()
            self.links[link.get_id()] = link


    def _update_existing_node(self, node, stored_node):

        if node.type.is_declared_type() and stored_node.type.is_referenced_type():
            node.status = self._status_new()
            self.nodes[node.get_id] = node
        elif node.type.is_referenced_type() and stored_node.type.is_declared_type():
            return # ignore
        elif node.type.is_declared_type() and stored_node.type.is_declared_type():
            if stored_node.status is self._status_new():
                return # skip, somewhow visited multiple times
            if node.node_hash_code != stored_node.node_hash_code:
                stored_node.status = Status.CHANGED
                stored_node.set_position_old(node.position[0], node.position[1])
            elif stored_node.status is Status.DELETED and self._status_new() is Status.ADDED:
                stored_node.status = Status.UNCHANGED
                stored_node.set_position_old(node.position[0], node.position[1])     
        elif stored_node.type.is_referenced_type():
            stored_node.status = Status.UNCHANGED
        else:
            stored_node.status = Status.CHANGED

    
    def add_new_node(self, node):
        if node.type.is_referenced_type():
            node.status = Status.UNCHANGED
        else:
            node.status = self._status_new()
        self.nodes[node.get_id()] = node
    

    def add_node(self, node):
        try:
            graph_node = self.nodes[node.get_id()]
            self._update_existing_node(node, graph_node)
        except KeyError:
            self.add_new_node(node)


    def _update_parent_nodes(self, node):
        try:
            parent_node = self.nodes[node.parent_node_id]
            if parent_node.status is Status.UNCHANGED:
                parent_node.status = Status.CHANGED
            self._update_parent_nodes(parent_node)
        except KeyError:
            pass
    

    # Used for generated nodes (currently not used).
    # def _update_child_nodes(self, node):
    #     filtered_nodes = [child_node for child_node in self.nodes.values() if node.get_id() == child_node.parent_node_id]
    #     for child_node in filtered_nodes:
    #         child_node.is_generated = True
    #         self._update_child_nodes(child_node)


    def cleanup(self):

        # update nodes with !unchanged links
        changed_links = [link for link in self.links.values() if link.status is not Status.UNCHANGED]
        for link in changed_links:
            try:
                node = self.nodes[link.source]
            except:
                # Functions in Python's standard library can trigger this.
                # For example random.random() is a function, but actually a method of a hidden Random class instance.
                continue
            if node and not node.type.is_referenced_type() and node.status is Status.UNCHANGED:
                node.status = Status.CHANGED

        # update parent nodes of !unchanged nodes
        for node in self.nodes.values():
            if node.status is not Status.UNCHANGED:
                self._update_parent_nodes(node)

        # update child nodes of @generated nodes (currently not used)
        # for node in self.nodes.values():
        #     if node.is_generated:
        #         self._update_child_nodes(node)
    

    def __str__(self):
        graph_repr = {}
        graph_repr['links'] = [link.json_helper() for link in self.links.values()]
        graph_repr['nodes'] = [node.json_helper() for node in self.nodes.values()]
        return json.dumps(graph_repr)
