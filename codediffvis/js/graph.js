const stylesRect = {
    'rx': d => NodeType.isTypeMethod(d.type) ? '1rem' : 0, // rounded corners for methods
    'fill': d => ColorHelper.getColor(d, settings['slider-colors']),
    'stroke-width': d => isNodeReviewed(d) ? "2px" : "4px",
    'height': '2rem'
};

// use in conjunction with normal rect to define a border for errors
const stylesErrorRectBorder = {
    'fill': 'none',
    'stroke': 'yellow',
    'stroke-dasharray': '5,5'
};

const stylesLine = {
    'stroke-dasharray': d => d.status != NodeStatus.UNCHANGED && (d.relation == NodeRelation.METHOD_CALL || d.relation == NodeRelation.FUNCTION_CALL) ? ('3, 3') : 'none',
    'stroke': d => settings['slider-colors'] ? 'rgb(192, 192, 192)' : ChangeBasedColor[d.status],
    'stroke-width': d => d.status != NodeStatus.UNCHANGED && (d.relation == NodeRelation.METHOD_CALL || d.relation == NodeRelation.FUNCTION_CALL) ? 3 : 2
    // 'marker-end': 'url(#arrow)'
};

const stylesText = {
    'font-weight': d => isNodeReviewed(d) ? "normal" : "bold",
    'fill': d => ColorHelper.getTextColor(d, settings['slider-colors']),
    'font-family': 'sans-serif',
    'font-size': '1em',
    'pointer-events': 'none'
};

const stylesTextParent = {
    'fill': d => 'black',
    'font-family': 'sans-serif',
    'font-size': '0.75em',
    'pointer-events': 'none'
};

const stylesCircle = {
    'fill': d => ColorHelper.getColor(d, settings['slider-colors']),
    'opacity': 0.25,
    'stroke': d => d.type == NodeType.TYPE_REFERENCE || d.type == NodeType.METHOD_REFERENCE || d.type == NodeType.FUNCTION_REFERENCE ? 'black' : 'none'
};

const stylesTextType = {
    'fill': d => ColorHelper.getTextColor(d, settings['slider-colors']),
    'font-family': 'sans-serif',
    'font-size': '0.75em',
    'pointer-events': 'none',
    'font-style': 'italic'
};

// When multiple languages are present in the graph, they can be toggled individually.
const languageSelectorStyles = {
	'boxStyle': {
		'position': 'absolute',
		'top': '0px',
		'right': '0px',
		'height': 'auto',
		'border-style': 'solid',
        'background': '#fff' // 'rgba(255, 255, 255, 0.8)'
	},

	'titleDivStyle': {
		'margin': '0px',
		'overflow': 'hidden',
		'border-bottom': '1px solid #eee',
		'width': '120px',
		'align-items': 'center',
		'justify-content': 'center'
	},

	'titleStyle': {
		'font-size': '1rem',
		'margin': '0.5rem auto',
		'text-align': 'center'
	},

	'paddedStyle': {
		'padding': '0 0.5rem'
	},

	'settingsFieldStyle': {
		'margin': '0.5rem 1rem 0.5rem auto'
	},

	'sliderContainerStyle': {
		'float': 'right',
		'margin': '0 0.5rem',
		'width': '1rem'
	},

	'switchStyle': {
		'position': 'relative',
		'display': 'inline-block',
		'width': '2rem',
		'height': '1rem'
	},

	'settingsSliderStyle': {
		'float': 'left',
		'opacity': '0',
		'width': '0',
		'height': '0'
	},

	'sliderStyle': {
		'position': 'absolute',
		'cursor': 'pointer',
		'top': '0',
		'left': '0',
		'right': '0',
		'bottom': '0',
		'background-color': '#ccc',
		'transition': '.3s'
	}
};


const stylesCommentType = {
    'font-family': 'sans-serif',
    'font-size': '1em',
    'fill': 'blue',
    'cursor': 'help',
    'text-shadow': '1px 0 0 black, 0 1px 0 black, -1px 0 0 black, 0 -1px 0 black'
};


// Styling for warning (tool error) nodes.
const stylesErrorType = {
    'font-family': 'sans-serif',
    'font-size': '1.5em',
    'fill': 'yellow',
    'cursor': 'help',
    'text-shadow': '1px 0 0 black, 0 1px 0 black, -1px 0 0 black, 0 -1px 0 black'
};

// Gets opened when clicking on a warning (tool error) node.
const errorWindowStyles = {
	'boxStyle': {
		'position': 'absolute',
		'top': '0px',
		'left': '0px',
		'height': 'auto',
		'border-style': 'solid',
        'border-width': '1px',
        'border-color': 'black',
        'width': '24rem',
        'background-color': 'rgb(255, 255, 0, 0.8)',
        'overflow-wrap': 'break-word'
	},

    'closeButtonStyle': {
        'position': 'absolute',
        'right': '0px',
        'width': '2em',
        'height': '2em',
        'font-size': '1em'
    },

	'titleDivStyle': {
		'margin': '0px',
		'overflow': 'hidden',
		//'border-bottom': '1px solid black',
		//'width': '20rem',
		'align-items': 'center',
		'justify-content': 'center'
	},

	'titleStyle': {
		'font-size': '1rem',
		'margin': '0.5rem auto',
		'text-align': 'center'
	},

    'separatorStyle': {
        'margin': '0 4em',
        'width': '16em',
        'height': '1px',
        'align-items': 'center',
        'justify-content': 'center',
        'background-color': '#000'
    },

    'errorMessageStyle': {
        'margin': '0.25rem'
    }
};


var draggingNode = false;

class Graph {

    constructor(data, graphWindow, svg) {
        this.data = data;
        this.tree = new NodeTree(data);
        this.graphWindow = graphWindow;
        this.svg = svg;
        this.nodes = this.tree.nodes;
        this.links = this.tree.links;
		this.activeLanguages = new Set((function* (nodes) {for (var node of nodes) {if (node.type != NodeType.UNKNOWNFILE) {yield node.language;}}})(this.nodes)); // :D
        // this.activeLanguages = new Set(this.nodes.filter(node => node.type != NodeType.UNKNOWNFILE).map(node => node.language));
        this._updateTree();

        // End of line marker (arrow).
        this.svg.append("defs").append("marker")
                .attr("id", 'arrow')
                .attr("viewBox", "0 -5 10 10")
                .attr("refX", 8)
                .attr("refY", 0)
                .attr("markerWidth", 10)
                .attr("markerHeight", 10)
                .attr('markerUnits', 'userSpaceOnUse')
                .attr("orient", "auto")
                //.attr('fill', 'red')
                //.style('fill', 'red')
                //.style("stroke-width", 1)
            .append("path")
                .attr("d", "M0,-5L10,0L0,5")

        this.simulation = d3.forceSimulation(this.nodes)
            .force('link', d3.forceLink(this.links).id(d => d.id).distance(50).strength(0.1))
            .force('charge', d3.forceManyBody().strength(-500))
            .force('forceX', d3.forceX(windowWidth / 2).strength(0.05))
            .force('forceY', d3.forceY(windowHeight / 2).strength(0.05))
            .force('center', d3.forceCenter(windowWidth / 2, windowHeight / 2))
            .force('collision', rectCollide())
            .nodes(this.nodes)

        this.container = this.svg.append('g').attr('class', 'container');
        this.simulation.on('tick', () => this._tick());
        this.simulation.velocityDecay(0.75);

        this.zoom = d3.zoom().on('zoom', () => {
            var nodeX = this.nodes.map(n => n.x);
            var nodeY = this.nodes.map(n => n.y);
            var minX = Math.min(...nodeX),
                minY = Math.min(...nodeY),
                maxX = Math.max(...nodeX),
                maxY = Math.max(...nodeY);
            var distX = 200 + 0.1 * (maxX - minX) / 2,
                distY = 200 + 0.1 * (maxY - minY) / 2;
            this.zoom.translateExtent([
                [minX - distX, minY - distY],
                [maxX + distX, maxY + distY]
            ])
            return this.container.attr('transform', d3.event.transform)
        }).scaleExtent([0, 2])
        this.svg.call(this.zoom)
            .on('dblclick.zoom', null);
    }

    start = () => {
        this._draw();
    }

    restart = changedKey => {
        this._update(changedKey);
        this._redraw();
    }
    
    updateForceCenter = () => {
        this.simulation.force('center', d3.forceCenter(windowWidth / 2, windowHeight / 2));
        this.simulation.alphaTarget(0.002).restart()
    }

    focus = node => {
        this.svg.transition().duration(500)
            .call(this.zoom.translateTo, node.x, node.y)
    }

    addCommentIndicators = (perNodeLineNumbers, reviewDiscussions) => {
        this.container.selectAll('g.node')
            .each(function (d, i) {

                if (!reviewDiscussions.has(d.id)) {
                    return;
                }

                let lineNumbers = perNodeLineNumbers.get(d.id);
                let allLineDiscussions = reviewDiscussions.get(d.id);

                d.reviewDiscussions = allLineDiscussions;
                let commentIndicator = d3.select(this).append("text").attr('class', 'commentType').text('C').styles(stylesCommentType);

                let titleText = "";

                allLineDiscussions.forEach((lineDiscussion, lineIndex) => {
                    titleText += '***** Line ' + lineNumbers[lineIndex] + ' *****\n';

                    lineDiscussion.forEach((discussion, discussionIndex) => {
                        discussion.forEach((comment, commentIndex) => {
                            titleText += commentIndex > 0 ? '\n' : '';
                            titleText += '>'.repeat(commentIndex) + ' ' + comment;
                        })
                        titleText += discussionIndex < discussion.length - 1 ? '\n----------\n' : '';
                    })
                    titleText += lineIndex < lineDiscussion.length - 1 ? '\n\n' : '';
                })

                commentIndicator.append('title').text(titleText);
            });
        
            this._tick(); // correctly set comment indicator positions
    }

    _filterAndUpdateNodes = changedKey => {
        if (changedKey == 'slider-unknownfiles') {
            if (settings[changedKey]) {
                var nodesUnknownFiles = this.tree.nodes.filter(d => d.type == NodeType.UNKNOWNFILE);
                this._pushNodes(this.nodes, nodesUnknownFiles);
            } else {
                this.nodes = this.nodes.filter(d => d.type != NodeType.UNKNOWNFILE);
            }
        } else if (changedKey == 'slider-generated') {
            if (settings[changedKey]) {
                var nodesGenerated = this.tree.nodes.filter(d => d.status != NodeStatus.UNCHANGED && d.isGenerated && this.activeLanguages.has(d.language));
                this._pushNodes(this.nodes, nodesGenerated);
            } else {
                this.nodes = this.nodes.filter(d => !d.isGenerated);
            }
        } else if (changedKey == 'slider-methods') {
            if (!settings[changedKey]) {
                var nodesMethodsUnchanged = this.tree.nodes.filter(d => d.type == NodeType.METHOD && d.status != NodeStatus.UNCHANGED && this.activeLanguages.has(d.language))
                this._pushNodes(this.nodes, nodesMethodsUnchanged);
            } else {
                this.nodes = this.nodes.filter(d => d.type != NodeType.METHOD);
            }
        } else if (changedKey == 'slider-warnings') {
            if (settings[changedKey]) {
                var nodesErrors = this.tree.nodes.filter(d => d.type == NodeType.TOOLERROR && d.status != NodeStatus.UNCHANGED && this.activeLanguages.has(d.language))
                this._pushNodes(this.nodes, nodesErrors);
            } else {
                this.nodes = this.nodes.filter(d => d.type != NodeType.TOOLERROR);
            }
        }
    }
	
	_filterNodes = nodesToFilter => {
		var filter = [NodeType.CLASS, NodeType.INTERFACE, NodeType.ABSTRACT_CLASS, NodeType.FUNCTION, NodeType.SCRIPT];
        if (settings['slider-unknownfiles']) {
            filter.push(NodeType.UNKNOWNFILE);
        }
        if (!settings['slider-methods']) {
            filter.push(NodeType.METHOD)
        }
        if (settings['slider-warnings']) {
            filter.push(NodeType.TOOLERROR)
        }
		
		return nodesToFilter.filter(
            n => {
                var showGeneratedFiles = true;
                if (!settings['slider-generated']) {
                    showGeneratedFiles = !n.isGenerated;
                }
                return n.status != NodeStatus.UNCHANGED && filter.includes(n.type) && showGeneratedFiles && (this.activeLanguages.has(n.language) | n.type == NodeType.UNKNOWNFILE);
            }
        );
	}
	
    _filterNodesStart = () => {
		this.nodes = this._filterNodes(this.tree.nodes);
    }


    _positionNodesInitial = () => {

        //position main nodes (top-level classes/functions, scripts)
        var radius = 200 + 20 * this.nodes.length;
        var mainNodes = this.nodes.filter(n => n.classNodeId == undefined);
        mainNodes.forEach((n, i) => {
            var angle = 2 * Math.PI / mainNodes.length * i;
            n.x = radius * Math.sin(angle);
            n.y = radius * Math.cos(angle);
        });

        //position non main nodes that haven't been placed yet (e.g., nested classes/functions)
        radius = 500;
        var nonMainNodes = this.nodes.filter(n => n.classNodeId != undefined && !NodeType.isTypeMethod(n.type) && n.x == undefined && n.y == undefined);
        nonMainNodes.forEach((n, i) => {
            var angle = 2 * Math.PI / nonMainNodes.length * i;
            var mainNode = mainNodes.find(d => d.id == n.classNodeId);
            n.x = radius * Math.sin(angle) + (mainNode == undefined ? 0 : mainNode.x);
            n.y = radius * Math.cos(angle) + (mainNode == undefined ? 0 : mainNode.y);
        });



        let methodsCollectedByParent = new Map();

        this.nodes.filter(n => n.classNodeId != undefined && NodeType.isTypeMethod(n.type))
            .forEach(methodNode => {
                if (!methodsCollectedByParent.has(methodNode.parentNodeId)) {
                    methodsCollectedByParent.set(methodNode.parentNodeId, new Array());
                }
                methodsCollectedByParent.get(methodNode.parentNodeId).push(methodNode);
            });
        

        methodsCollectedByParent.forEach((methodNodes, parentNodeId) => {

            let methodByConnectionDirection = new Map();
            let parentNode = this.nodes.find(d => d.id == parentNodeId);


            methodNodes.forEach(methodNode => {
                let connectedMainNodes = [];
                let callingNodesNames = this.links.filter(l => l.relation == NodeRelation.METHOD_CALL && (l.source == methodNode.id || l.target == methodNode.id)).map(l => l.source == methodNode.id ? l.target : l.source);

                callingNodesNames.forEach(nodeName => {

                    // Find the connected node.
                    let connectedPositionedNode = this.nodes.find(n => n.id == nodeName);

                    // Find the lowest already positioned node in the tree if any.
                    while (connectedPositionedNode != undefined && connectedPositionedNode.x == undefined && connectedPositionedNode.y == undefined) {
                        connectedPositionedNode = this.nodes.find(n => n.id == connectedPositionedNode.parentNodeId);
                    }

                    if (connectedPositionedNode != undefined) {
                        connectedMainNodes.push(connectedPositionedNode);
                    }
                });

                // Direction of summed up links.
                let posX = 0;
                let posY = 0;

                connectedMainNodes.forEach(mainNode => {

                    // Angle in radians, starting with 0 at the bottom and increasing clockwise to 2*pi.
                    let nodeAngle = Math.atan((mainNode.y - parentNode.y) / (parentNode.x - mainNode.x));
                
                    // points  to left (-x)
                    if (mainNode.x < parentNode.x) {
                        let distX = -Math.cos(nodeAngle);
                        let distY = mainNode.y < parentNode.y ? -Math.sqrt(1 - Math.pow(distX, 2)) : Math.sqrt(1 - Math.pow(distX, 2));
                        posX += distX;
                        posY += distY;
                    }

                    // points to right (+x)
                    else {
                        let distX = Math.cos(nodeAngle);
                        let distY = mainNode.y < parentNode.y ? -Math.sqrt(1 - Math.pow(distX, 2)) : Math.sqrt(1 - Math.pow(distX, 2));
                        posX += distX;
                        posY += distY;
                    }

                    posX /= connectedMainNodes.length; // normalize length
                    posY /= connectedMainNodes.length; // normalize length
                });

                methodByConnectionDirection.set(methodNode, [posX, posY]);
            });

            // Sort by weight (1 link in 1 direction = weight 1, 2 links 90 deg apart = weight root(2)/2 -> single direction > multiple directions)
            let sortedByWeightMap = new Map([...methodByConnectionDirection].sort((a, b) => {
                let lengthA = Math.pow(a[1][0], 2) + Math.pow(a[1][1], 2);
                let lengthB = Math.pow(b[1][0], 2) + Math.pow(b[1][1], 2);
                return lengthA > lengthB ? -1 : 1;
            }));

            // Keep track of already positioned nodes.
            let positionedNodesAngles = new Array();

            sortedByWeightMap.forEach((connectionDirection, methodNode) => {

                // If [0,0] (no connection), randomly set direction and let the algorithm find a free spot.
                if (connectionDirection[0] == 0 && connectionDirection[1] == 0) {
                    connectionDirection[0] = Math.random();
                    connectionDirection[1] = Math.random();
                }

                // map it to interval [0, 2*pi], with 0 at bottom of unit circle and increasing clockwise
                let angle = Math.atan(-connectionDirection[1] / connectionDirection[0]) + Math.PI / 2;
                if (connectionDirection[0] >= 0) {
	                angle = 2*Math.PI - angle;
                }
                else {
                    angle = Math.PI - angle;
                }

                // Keep nodes a certain angle apart.
                let minAngularDistance = Math.PI / sortedByWeightMap.keys.length;


                // angular offset to test for too close nodes
                let clockwiseAngle = 0;
                let counterClockWiseAngle = 0;

                // Start from original angle, then move away from it to find the closest (in degrees) free spot.
                while (Math.min(clockwiseAngle, counterClockWiseAngle) < Math.PI) {

                    let angleToCheck = angle;

                    if (clockwiseAngle < counterClockWiseAngle) {
                        angleToCheck += clockwiseAngle;
                    }
                    else {
                        angleToCheck -= counterClockWiseAngle;
                    }

                    if (angleToCheck < 0) {
                        angleToCheck += 2*Math.PI;
                    }
                    else if (angleToCheck > 2*Math.PI) {
                        angleToCheck -= 2*Math.PI;
                    }

                    let tooCloseAngle = positionedNodesAngles.find(positionedAngle => Math.min(angleToCheck-positionedAngle, positionedAngle-angleToCheck) < minAngularDistance);

                    if (tooCloseAngle == undefined) {
                        angle = angleToCheck;
                        break;
                    }

                    // too close to already positioned node -> calculate closest angle at minAnglularDistance away
                    else {
                        let angularDiff = angleToCheck - tooCloseAngle;

                        // next closest angle that isn't too close is clockwise
                        if ((angleToCheck < tooCloseAngle && Math.abs(angularDiff) > minAngularDistance) || (angleToCheck > tooCloseAngle && angularDiff < minAngularDistance)) {
                            if (clockwiseAngle < counterClockWiseAngle) {
                                clockwiseAngle += (minAngularDistance - Math.abs(angularDiff));
                            }
                            else {
                                counterClockWiseAngle += minAngularDistance + Math.abs(angularDiff);
                            }
                        }

                        // next closest angle that isn't too close is counterclockwise
                        else {
                            if (clockwiseAngle < counterClockWiseAngle) {
                                clockwiseAngle += Math.abs(angularDiff) + minAngularDistance;
                            }
                            else {
                                counterClockWiseAngle += (minAngularDistance - Math.abs(angularDiff));
                            }
                        }
                    }
                }

                positionedNodesAngles.push(angle);

                let radius = 100;
                methodNode.x = radius * -Math.sin(angle) + (parentNode == undefined ? 0 : parentNode.x);
                methodNode.y = radius * Math.cos(angle) + (parentNode == undefined ? 0 : parentNode.y);
            });
        });
        

        //position methods
        // radius = 100;
        // var methodNodes = this.nodes.filter(n => n.classNodeId != undefined && NodeType.isTypeMethod(n.type));
        // methodNodes.forEach((n, i) => {
        //     var angle = 2 * Math.PI / methodNodes.length * i;
        //     var parentNode = mainNodes.find(d => d.id == n.parentNodeId);
        //     n.x = radius * Math.sin(angle) + (parentNode == undefined ? 0 : parentNode.x);
        //     n.y = radius * Math.cos(angle) + (parentNode == undefined ? 0 : parentNode.y);
        // });
    }


    _filterAndUpdateLinks = () => {

        // Function to decide which link between two nodes to pick if there are multiple links.
        // This can occurr when a function defines a nested function and calls it.
        // Current ordering is NodeRelation.FUNCTION < NodeRelation.FUNCTION_CALL because structural dependencies are signified by parentNodeId.
        let getPriorityLink = (link1, link2) => {
            if (link1.relation != "FUNCTION") {
                return link1;
            }
            return link2;
        }

        let linksMap = new Map();

        // group links that connect the same source and target
        this.tree.links.forEach(link => {

            if (!this.nodes.find(n => n.id == link.source || n == link.source) || !this.nodes.find(n => n.id == link.target || n == link.target)) {
                return; // Ignore links for unknown nodes.
            }

            let key = "";
            if (typeof(link.source) == 'string') {
                // id not matched to link object (initial loading)
                key = link.source < link.target ? link.source + link.target : link.target + link.source; // sort links to prevent overlapping
            }
            else {
                // id matched to link object (reloading)
                key = link.source.id < link.target.id ? link.source.id + link.target.id : link.target.id + link.source.id; // sort links to prevent overlapping
            }
            
            if (!linksMap.has(key)) {
                linksMap.set(key, link); // no previous link between these nodes found
            }
            else {
                linksMap.set(key, getPriorityLink(linksMap.get(key), link)); // multiple links between these nodes -> pick one
            }
        });

        this.links = Array.from(linksMap.values());

    }

    _update = (changedKey) => {
        this._filterAndUpdateNodes(changedKey);
        this._filterAndUpdateLinks();
        ColorHelper.updatePackageColor(this.nodes.map(n => n.packageName));
    }

    _updateTree = () => {
        this._filterNodesStart();
        this._positionNodesInitial();
        this._filterAndUpdateLinks();
        ColorHelper.updatePackageColor(this.nodes.map(n => n.packageName));
    }

    _tick = () => {
		console.log('tick')
        this.container.selectAll('circle.circle')
            .attr('cx', d => d.x)
            .attr('cy', d => d.y)
            .attr('r', d => d.radius);

        this.container.selectAll('rect')
            .attr('x', d => d.x - d.width2)
            .attr('y', d => d.y - remToPixel(1))
            .attr('width', d => d.width);

        this.container.selectAll('text.name')
            .attr('x', d => d.x - d.width2 + remToPixel(1.25))
            .attr('y', d => d.y + remToPixel(0.3));

        this.container.selectAll('text.parent')
            .attr('x', d => d.x - d.widthParent2 + remToPixel(1))
            .attr('y', d => d.y - remToPixel(1.2));

        this.container.selectAll('line')
            .attr('x1', d => d.source.x)
            .attr('y1', d => d.source.y)
            //.attr('x2', d => d.target.x - 10)
            //.attr('y2', d => d.target.y - 10);

        this.container.selectAll('line').each(function (d) {

            if (d.relation == "METHOD") {
                d3.select(this)
                    .attr('x2', d => d.target.x)
                    .attr('y2', d => d.target.y);
                return;
            }

            // Assume a node is rectangular -> set end of line on this border.

            let dx = d.target.x - d.source.x;
            let dy = d.target.y - d.source.y;

            let angle = Math.asin(dy / Math.sqrt(dx*dx + dy*dy));

            let x2, y2;

            // line intersects top/bottom
            if (Math.abs(Math.sin(angle) * ((d.target.width / 2) / Math.sin(Math.PI / 2 - angle))) > remToPixel(2) / 2) {
                x2 = Math.cos(angle) * ((remToPixel(2) / 2) / Math.cos(Math.PI / 2 - angle));
                y2 = remToPixel(2) / 2; // height / 2
                if (d.target.y < d.source.y) {
                    x2 = -x2; // Calculated for target below source -> correct
                }
            }
            // line intersects side
            else {
                x2 = d.target.width / 2;
                y2 = Math.sin(angle) * ((d.target.width / 2) / Math.sin(Math.PI / 2 - angle));
                if (d.target.y < d.source.y) {
                    y2 = -y2; // Calculated for target below source -> correct
                }
            }

            if (d.target.x > d.source.x) {
                x2 = -x2;
            }

            if (d.target.y > d.source.y) {
                y2 = -y2;
            }

            d3.select(this)
                .attr('x2', d => d.target.x + x2)
                .attr('y2', d => d.target.y + y2);
        });


        this.container.selectAll('text.textType')
            .attr('x', d => d.x - d.width2 + remToPixel(0.5))
            .attr('y', d => d.y + remToPixel(0.25));
        
        this.container.selectAll('text.errorType')
            .attr('x', d => d.x - d.width2 + remToPixel(0.1))
            .attr('y', d => d.y - remToPixel(0.5));
        
        this.container.selectAll('text.commentType')
            .attr('x', d => d.x + d.width2 - remToPixel(0.4))
            .attr('y', d => d.y - remToPixel(0.5));
    }

    _redraw = () => {
        this.simulation.nodes(this.nodes);
        this.simulation.force('link')
            .links(this.links)
            .initialize(this.nodes);

        var windowBody = d3.select(this.graphWindow.document.body);
        windowBody.selectAll('g.node').remove();
		windowBody.selectAll('div').remove();
        windowBody.selectAll('g.node').data(this.nodes).join();
        windowBody.selectAll("line").data(this.links).join();
        windowBody.selectAll("undefined").remove();

        this._draw();
        this.simulation.alphaTarget(0.002).restart()
    }


    _drawErrorWindow = (errorsParentName, errors) => {

        // add stylesheet if not already present        
        addErrorWindowStyleSheet(this.graphWindow);

        // remove old windows
        d3.select(this.graphWindow.document.body).selectAll('.error-window').remove();

        let errorWindow = d3.select(this.graphWindow.document.body).append('div').styles(errorWindowStyles.boxStyle).attr('class', 'error-window');

        errorWindow.append('div').attr('class', 'close-button').styles(errorWindowStyles.closeButtonStyle);
        
        let closeBtn = errorWindow.append('button').styles(errorWindowStyles.closeButtonStyle).text('×');
        closeBtn.on('click', () => {errorWindow.remove();})

        errorWindow
            .append('div').styles(errorWindowStyles.titleDivStyle)
			.append('h1').styles(errorWindowStyles.titleStyle).text('Tool errors in file ' + errorsParentName);

        errorWindow.append('div').styles(errorWindowStyles.separatorStyle);
        
        errors.forEach(error => {
            errorWindow.append('p').styles(errorWindowStyles.errorMessageStyle).text(error.notes);
        });
    }


    _draw = () => {
        var nodeIds = this.nodes.map(n => n.id);
        var treeNodesMap = this.tree.nodesMap;

        this.container.selectAll('line')
            .data(this.links)
            .join('line').attr('class', 'links')
            .styles(stylesLine)
            .filter(l => l.relation != "METHOD")
            .attr('marker-end', 'url(#arrow)');

        var activeLanguages = this.activeLanguages; // used to assign border color if needed

        this.container.selectAll('g.node').raise()
            .data(this.nodes)
            .join("g").attr("class", 'node')
            .each(function (d, i) {
                
                let rect = d3.select(this).append("rect").attr('class', 'rect').styles(stylesRect);
                
                if (activeLanguages.size > 1) {
                    rect.styles({'stroke': ColorHelper.getColorByLanguage(d.language)});
                }

                var text = d3.select(this).append("text").attr('class', 'name').text(d => d.name).styles(stylesText);
                d.width = text.filter(t => t.index == d.index).node().getBBox().width + remToPixel(2);
                d.width2 = d.width / 2;
                d.height = remToPixel(2);

                if (d.reviewDiscussions.length > 0) {
                    let commentIndicator = d3.select(this).append("text").attr('class', 'commentType').text('C').styles(stylesCommentType);
                    commentIndicator.append('title').text(d.reviewDiscussions);
                }

                // skip UNKNOWNFILE nodes
                if (d.language == '') {
                    return;
                }
                
                let currentGraph = languageSpecificElements.get('graphs').get(getKeyMatch(d.language));

                let linked_error_nodes = currentGraph.data.nodes.filter(node => {
                    return d.links.includes(node.id) && node.type == NodeType.TOOLERROR;
                });
                
                if (linked_error_nodes.length > 0) {
                    d3.select(this).append("rect").attr('class', 'rect').styles(stylesRect).styles(stylesErrorRectBorder); // add checkered border
                    //rect.on('click', d => currentGraph._drawErrorWindow(d.name, linked_error_nodes));

                    let warningMark = d3.select(this).append("text").attr('class', 'errorType').text('?').styles(stylesErrorType);
                    warningMark.on('click', d => currentGraph._drawErrorWindow(d.name, linked_error_nodes));

                    let warningText = '';
                    linked_error_nodes.forEach(error => {
                        warningText += error.notes + '\n';
                    });
                    warningMark.append('title').text(warningText);
                }

                if (d.type == NodeType.TOOLERROR) {
                    d3.select(this).append("rect").attr('class', 'rect').styles(stylesRect).styles(stylesErrorRectBorder); // add checkered border
                }

                if (!NodeType.isTypeMethod(d.type) && d.classNodeId != null) {
                    var textParent = d3.select(this).append("text").attr('class', 'parent').text(d => treeNodesMap.get(d.classNodeId).name).styles(stylesTextParent);
                    d.widthParent = textParent.filter(t => t.index == d.index).node().getBBox().width + remToPixel(2);
                    d.widthParent2 = d.widthParent / 2;
                }

                if (!NodeType.isTypeMethod(d.type)) {
                    var methods = d.children.filter(c => NodeType.isTypeMethod(c.type) && nodeIds.includes(c.id)).length
                    d.radius = methods > 0 ? d.width2 + remToPixel(1) + methods * remToPixel(1) + 2 : 0;
                    d3.select(this).append("circle").attr('class', 'circle').styles(stylesCircle).lower();
                }

                if (NodeType.isDeclaredType(d.type) && d.type != NodeType.METHOD || d.type == NodeType.SCRIPT) {
                    d3.select(this).append('text').attr('class', 'textType').text(d => d.type[0]).styles(stylesTextType);
                }
            })
            .on('mouseover', (d) => this._onNodeHover(d))
            .on('mouseout', () => this._onHoverExit())
            .on('click', d => this._onNodeClick(d))
            .on('contextmenu', d => this._onNodeContextMenu(d))
            .call(drag(this.simulation));
		
		
		var totalLanguagesSet = new Set();
		this.tree.nodes.forEach(node => { if (node.type != NodeType.UNKNOWNFILE) {totalLanguagesSet.add(node.language);}});
		//var activeLanguagesSet = new Set();
        // TODO: Check if it can be removed.
		this.nodes.forEach(node => {if (node.type != NodeType.UNKNOWNFILE) {this.activeLanguages.add(node.language);}})
		this._drawLanguageSelector(Array.from(totalLanguagesSet), Array.from(this.activeLanguages));
    }
	
	
	_toggleLanguage = (language, isSelected) => {
		if (isSelected) {
			this.activeLanguages.add(language);
			var nodesLanguage = this.tree.nodes.filter(d => d.language == language);
			nodesLanguage = this._filterNodes(nodesLanguage);
            this._pushNodes(this.nodes, nodesLanguage);
		}
		else {
			this.activeLanguages.delete(language);
			this.nodes = this.nodes.filter(d => d.language != language);
		}
		
		this._filterAndUpdateLinks();
        ColorHelper.updatePackageColor(this.nodes.map(n => n.packageName));
		this._redraw();
	}
	
	
	
	_drawLanguageSelector = (totalLanguageNames, activeLanguageNames) => {
		
		if (!totalLanguageNames || totalLanguageNames.length < 2) {
			d3.select(this.graphWindow.document.body).selectAll("#language-selector").remove();
			return;
		}
		
		var languageSelector = d3.select(this.graphWindow.document.body)
			.append('div').attr('id', 'language-selector').styles(languageSelectorStyles.boxStyle)

		languageSelector
			.append('div').styles(languageSelectorStyles.titleDivStyle)
			.append('h1').styles(languageSelectorStyles.titleStyle).text('Languages')
		
		
		totalLanguageNames.forEach(languageName => {
			
			let languageSettings = languageSelector
				.append('div').styles(languageSelectorStyles.paddedStyle)
				.append('div').styles(languageSelectorStyles.settingsFieldStyle)
            
			languageSettings.append('label').text(languageName).styles({'color': ColorHelper.getColorByLanguage(languageName), 'font-weight': 'bold'}) //.styles({'background-color': ColorHelper.getColorByLanguage(languageName)});

			let languageSwitch = languageSettings
				.append('div').styles(languageSelectorStyles.sliderContainerStyle)
				.append('label').styles(languageSelectorStyles.switchStyle)
			
			languageSwitch.append('input').attr('type', 'checkbox').property('checked', activeLanguageNames.includes(languageName)).styles(languageSelectorStyles.settingsSliderStyle)
			languageSwitch.append('span').styles(languageSelectorStyles.sliderStyle).attr('class', 'slider')
			
			languageSwitch.on('change', () => this._toggleLanguage(languageName, d3.event.target.checked))
		});
	}


    _onNodeHover = node => {
        if (draggingNode) {
            return;
        }
        isHovering = true;
        var isNodeClickable = isClickable(this._getClickableElement(node));
        if (isNodeClickable) {
            this.svg.style('cursor', 'grab');
        }
        this.container.selectAll('text.name').style('text-decoration', o => o == node && isNodeClickable ? 'underline' : 'none');
        if (isHighlightLocked) {
            return;
        }
        var connectedNodes = this._getConnectedNodes(node);
        var connectedLinks = this.links.filter(l => connectedNodes.includes(l.source) && connectedNodes.includes(l.target));

        this.container.selectAll('text').filter(o => !connectedNodes.includes(o))
            .style('color', 'black').style('opacity', 0.1)
        this.container.selectAll('rect.rect,line,circle')
            .filter(o => !connectedNodes.includes(o) && !connectedLinks.includes(o))
            .style('opacity', 0.1)
        this.container.selectAll('line').filter(o => connectedLinks.includes(o)).raise()
        this.container.selectAll('g.node').filter(o => connectedNodes.includes(o)).raise()
        this.container.selectAll('g.node').filter(o => connectedNodes.includes(o) && NodeType.isTypeMethod(o.type)).raise()
    }

    _onHoverExit = () => {
        if (draggingNode) {
            return;
        }
        isHovering = false;
        if (isHighlightLocked) {
            return;
        }
        this.svg.style('cursor', 'move');
        this.container.selectAll('text.name').styles(stylesText).style('opacity', 1).style('text-decoration', 'none');
        this.container.selectAll('text.parent').styles(stylesTextParent).style('opacity', 1).style('text-decoration', 'none');
        this.container.selectAll('rect.rect,line').style('opacity', 1)
        this.container.selectAll('circle.circle').style('opacity', stylesCircle['opacity'])
        this.container.selectAll('text.textType').styles(stylesTextType).style('opacity', 1);
        this.container.selectAll('text.errorType').styles(stylesErrorType).style('opacity', 1);
        this.container.selectAll('text.commentType').styles(stylesCommentType).style('opacity', 1);
        this.container.selectAll('g.node').raise();
        this.container.selectAll('g.node').filter(d => NodeType.isTypeMethod(d.type)).raise();
    }

    _getConnectedNodes = node => {
        var connectedNodes = [node];
        if (node.type == NodeType.METHOD) {
            var methodCallNodes = this._visibleChildren(node).filter(child => child != node
                && NodeType.isTypeMethod(child.type)
                && this._visibleChildren(child).find(b => !NodeType.isTypeMethod(b.type)));
            this._pushNodes(methodCallNodes, methodCallNodes.flatMap(m => this._visibleChildren(m).filter(o => !NodeType.isTypeMethod(o.type))));
            this._pushNodes(methodCallNodes, this._visibleChildren(node).filter(c => !NodeType.isTypeMethod(c.type)));
            this._pushNodes(connectedNodes, methodCallNodes);
        } else {
            this._pushNodes(connectedNodes, this._visibleChildren(node));
        }
        return connectedNodes;
    }

    _visibleChildren = node => {
        return node.children.filter(child => this.nodes.includes(child) && node.links.find(l => l == child.id));
    }

    _onNodeClickExpand = node => {

        var dataChanged = false;
        var methodCallNodes;

        if (node.type == NodeType.METHOD && node.status != NodeStatus.UNCHANGED) {
            methodCallNodes = node.children.filter(child => child != node && (NodeType.isTypeMethod(child.type)) && child.children.find(grandChild => !NodeType.isTypeMethod(grandChild.type)));
            this._pushNodes(methodCallNodes, [...new Set(methodCallNodes.flatMap(method => method.children.filter(child => !NodeType.isTypeMethod(child.type))))]);
            dataChanged = this._pushNodes(this.nodes, methodCallNodes, node);
        }
        else if (NodeType.isDeclaredType(node.type)) {
            methodCallNodes = node.children.filter(grandChild => grandChild.status != NodeStatus.UNCHANGED)
            dataChanged = this._pushNodes(this.nodes, methodCallNodes, node);
        }
        
        if (dataChanged) {
            node.methodCallNodes = methodCallNodes;
            this._filterAndUpdateLinks();
            this._redraw();
        }
    }

    _onNodeContextMenu = node => {
        d3.event.preventDefault();
        if (Array.isArray(node.methodCallNodes) && node.methodCallNodes.length) {
            this.nodes = this.nodes.filter(o => !node.methodCallNodes.includes(o));
            node.methodCallNodes = [];
        }
        this.nodes = this.nodes.filter(o => o != node);
        this._filterAndUpdateLinks();
        this._redraw();
    }

    _onNodeClick = node => {
        d3.event.preventDefault();
        if (isClickExpand) {
            isClickExpand = false;
            this._onNodeClickExpand(node);
            return;
        }
        var element = this._getClickableElement(node);
        if (isClickable(element)) {
            element.click();
            node.clicked = true;
            node.width = this.container.selectAll('text.name')
                .style('font-weight', text => isNodeReviewed(text) ? "normal" : "bold")
                .filter(t => t.index == node.index).node().getBBox().width + remToPixel(2);
            node.width2 = node.width / 2;
            this.container.selectAll('rect')
                .style('stroke-width', rect => isNodeReviewed(rect) ? "1px" : "2px");
            this._tick(); // force a tick
        }
    }

    _getClickableElement = d => {
        if (NodeType.isReferencedType(d.type)) {
            return null;
        }
        return getClickableElement(d.filePath, d.declaringScopesName != null ? d.position[0] : null)
    }

    _pushNodes = (nodes, newNodes, reference) => {
        newNodes = newNodes.filter(d => !nodes.includes(d));
        if (newNodes.length == 0) {
            return false;
        }
        newNodes.forEach(d => {
            if (d.x != undefined || d.y != undefined) {
                return;
            }
            if (reference == undefined) {
                d.x = windowWidth / 2;
                d.y = windowHeight / 2;
            } else {
                var a = Math.floor(Math.random() * Math.floor(360));
                d.x = reference.x + Math.cos(a) * reference.radius;
                d.y = reference.y + Math.sin(a) * reference.radius;
            }
        });
        nodes.push(...newNodes);
        ColorHelper.updatePackageColor(this.nodes.map(n => n.packageName));
        return true;
    }
}

drag = simulation => {
    var isLockedBeforeDragging = false;

    dragStart = node => {
        isLockedBeforeDragging = isHighlightLocked;
        isHighlightLocked = true;
        if (!d3.event.active) {
            simulation.alphaTarget(0.01).restart();
        }
        node.fx = node.x;
        node.fy = node.y;
        draggingNode = true;
    }

    dragging = node => {
        node.fx = d3.event.x;
        node.fy = d3.event.y;
    }

    dragEnd = node => {
        node.fx = null;
        node.fy = null;
        if (!isLockedBeforeDragging) {
            isHighlightLocked = false;
        }
        draggingNode = false;
        setTimeout(() => simulation.stop(), 100);
    }

    return d3.drag()
        .on('start', dragStart)
        .on('drag', dragging)
        .on('end', dragEnd);
}


// collision force
function rectCollide () {
    var nodes;

    force = () => {
        var node, parent, child;
        var xDelta, yDelta, xMinDist, yMinDist, xOverlap, yOverlap;
        var isTrappedInside = false, isKeepOutside = false;

        var tree = d3.quadtree(nodes, d => d.x, d => d.y);
        nodes.forEach(n => {
            node = n;
            tree.visit(apply);
        })

        function initCollisionParameters (data) {
            if (node.radius > data.radius) {
                parent = node;
                child = data;
            } else {
                parent = data;
                child = node;
            }

            xDelta = Math.abs(parent.x - child.x);
            yDelta = Math.abs(parent.y - child.y);
            xDeltaSign = Math.sign(parent.x - child.x);
            yDeltaSign = Math.sign(parent.y - child.y);

            xMinDist = parent.width2 + child.width2;
            yMinDist = (parent.height + child.height) / 2;
            xOverlap = xDelta - xMinDist;
            yOverlap = yDelta - yMinDist;
        }

        function isCollisionDetected () {
            return xOverlap < 0 && yOverlap < 0;
        }

        function isParentWithRadius () {
            return parent.radius > 0;
        }

        function handleCircularCollision () {
            if (isCollisionDetected() || !isParentWithRadius()) {
                // nodes are already overlapping or no radius is defined
                return;
            }

            var isChildMethodOfParent = NodeType.isTypeMethod(child.type) && child.parentNodeId == parent.id;
            var xMaxDist = 0, yMaxDist = 0;

            if (isChildMethodOfParent) {
                // trap child inside radius
                var dist = Math.sqrt(xDelta ** 2 + yDelta ** 2);
                if (dist > parent.radius) {
                    var scale = parent.radius / dist;
                    xMaxDist = scale * xDelta;
                    yMaxDist = scale * yDelta;
                    isTrappedInside = true;
                }
            } else {
                // keep child outside radius
                var xRadialDist = Math.abs(xDelta - child.width2);
                var yRadialDist = Math.abs(yDelta - child.height / 2);
                isKeepOutside = true;

                if (xDelta < child.width2 && yRadialDist < parent.radius) {
                    // special case where both edges are outside the circle but the child border intersects with the parent radius
                    xRadialDist = 0;
                    yMinDist = parent.radius;
                }
                var dist = Math.sqrt(xRadialDist ** 2 + yRadialDist ** 2);
                if (dist < parent.radius) {
                    var scale = parent.radius / dist;
                    xMinDist = scale * xDelta;
                    yMinDist = scale * yDelta;
                }
            }

            if (isTrappedInside) {
                xOverlap = xMaxDist - xDelta;
                yOverlap = yMaxDist - yDelta;

                // slow down if the nodes are too far apart
                xOverlap = xOverlap < -100 ? -(100 / xOverlap * (xOverlap + 100) + 100) : xOverlap;
                yOverlap = yOverlap < -100 ? -(100 / yOverlap * (yOverlap + 100) + 100) : yOverlap;
            } else {
                xOverlap = xDelta - xMinDist;
                yOverlap = yDelta - yMinDist;
            }
        }

        function isXCorrection () {
            // for circle collisions favor the bigger overlap as it results in a more natural behavior
            return isParentWithRadius() ? Math.abs(xOverlap) > Math.abs(yOverlap) && (isKeepOutside || isTrappedInside) : Math.abs(xOverlap) < Math.abs(yOverlap)
        }

        function apply (quad, x0, y0, x1, y1) {
            if (!quad.data || quad.data.index <= node.index) return false;

            initCollisionParameters(quad.data);
            handleCircularCollision();

            if (isCollisionDetected()) {
                // revert direction if it is a circle trap child inside collision
                if (isXCorrection()) {
                    var xChange = isTrappedInside ? -xDeltaSign * xOverlap : xDeltaSign * xOverlap;
                    parent.x -= isTrappedInside ? 0 : xChange / 2;
                    child.x += isTrappedInside ? xChange : xChange / 2;
                } else {
                    var yChange = isTrappedInside ? -yDeltaSign * yOverlap : yDeltaSign * yOverlap;
                    parent.y -= isTrappedInside ? 0 : yChange / 2;
                    child.y += isTrappedInside ? yChange : yChange / 2;
                }
            }

            isTrappedInside = false, isKeepOutside = false; //reset parameters
            return x0 > parent.x + xMinDist || y0 > parent.y + yMinDist
                || x1 < parent.x - xMinDist || y1 < parent.y - yMinDist;
        }
    }

    force.initialize = d => nodes = d;
    return force;
}
