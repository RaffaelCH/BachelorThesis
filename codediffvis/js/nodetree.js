const NodeType = Object.freeze({
    CLASS: 'CLASS',
    INTERFACE: 'INTERFACE',
    ABSTRACT_CLASS: 'ABSTRACT_CLASS',
    METHOD: 'METHOD',
	FUNCTION: 'FUNCTION',
    TYPE_REFERENCE: 'TYPE_REFERENCE',
    METHOD_REFERENCE: 'METHOD_REFERENCE',
	FUNCTION_REFERENCE: 'FUNCTION_REFERENCE',
	SCRIPT: 'SCRIPT',
    TOOLERROR: 'TOOLERROR',
    UNKNOWNFILE: 'UNKNOWNFILE',

    isDeclaredType: (nodeType) => {
        return [NodeType.CLASS, NodeType.INTERFACE, NodeType.ABSTRACT_CLASS, NodeType.METHOD, NodeType.FUNCTION].includes(nodeType);
    },
    isReferencedType: (nodeType) => {
        return [NodeType.TYPE_REFERENCE, NodeType.METHOD_REFERENCE, NodeType.FUNCTION_REFERENCE].includes(nodeType);
    },
    isTypeMethod: (nodeType) => {
        return [NodeType.METHOD, NodeType.METHOD_REFERENCE].includes(nodeType);
    }
});

const NodeStatus = Object.freeze({
    ADDED: 'ADDED',
    DELETED: 'DELETED',
    CHANGED: 'CHANGED',
    UNCHANGED: 'UNCHANGED'
});

const NodeRelation = Object.freeze({
    SUPERCLASS: 'SUPERCLASS',
    ENCLOSING_CLASS: 'ENCLOSING_CLASS',
    INTERFACE: 'INTERFACE',
    METHOD_CALL: 'METHOD_CALL',
    METHOD: 'METHOD',
    TYPE: 'TYPE',
	FUNCTION: 'FUNCTION',
	FUNCTION_CALL: 'FUNCTION_CALL',
    TOOLERROR: 'TOOLERROR'
});

const NodeLanguage = Object.freeze({
	JAVA: 'JAVA',
	PYTHON: 'PYTHON'
})

isNodeReviewed = (node) => {
    return node.clicked || node.status == NodeStatus.UNCHANGED || node.isGenerated
}

class NodeTree {
    constructor(data) {
        this.nodes = data.nodes.map(d => Object.create(d));
        this.links = data.links.map(d => Object.create(d));
        this.nodesMap = new Map(this.nodes.map(n => [n.id, n]));
        this.linksMap = new Map();
        this.links.forEach(l => {
            this.linksMap.set(l.source, this.linksMap.get(l.source) == undefined ? [l.target] : [...this.linksMap.get(l.source), l.target]);
            this.linksMap.set(l.target, this.linksMap.get(l.target) == undefined ? [l.source] : [...this.linksMap.get(l.target), l.source]);
        })
        this._treeTraversal();
    }

    _findClassNodeId = node => {
        // No parent or a SCRIPT node -> treat as top level node.
        if (node == undefined || !NodeType.isDeclaredType(node.type)) {
            return null;
        }
        if (node.parentNodeId == undefined || this.nodesMap.get(node.parentNodeId) == undefined) {
            return node.id;
        }
        return this._findClassNodeId(this.nodesMap.get(node.parentNodeId));
    }

    _treeTraversal = () => {
        this.nodes.forEach(n => {
            n.radius = 0;
            n.clicked = false;
            n.reviewed = false;
            n.reviewDiscussions = [];
            n.links = this.linksMap.get(n.id);
            n.links = n.links == undefined ? [] : n.links;
            n.children = n.links.map(l => this.nodesMap.get(l)).filter(n => n != undefined)
            n.classNodeId = this._findClassNodeId(this.nodesMap.get(n.parentNodeId)) // TODO: Adjust for Python.
        })
    }
}
