var highlightedNode;
var isHighlightLocked = false;
var isHovering = false;
var isClickExpand = false;


window.addEventListener('load', () => {
    checkForFileContent();
}, false);


var filesLengthOld = 0;

function checkForFileContent () {
    var files = Array.from(document.getElementsByClassName("file-holder"));
    if (files.length == 0 || filesLengthOld < files.length) {
        filesLengthOld = files.length;
        // wait 1 sec repeatedly until element creation
        return setTimeout(() => checkForFileContent(), 1000);
    } else {
        addCommentIndicators();
        files.forEach(e => e.addEventListener('mouseover', mouseOverCode));
        files.forEach(e => e.addEventListener('mouseleave', mouseLeaveCode));
    }
}


function getNodes() {
    let nodes = new Array();
    languageSpecificElements.get('graphs').forEach(graph => {
        graph.nodes.forEach(node => nodes.push(node));
    });
    return nodes
}


// Converts filepaths to a normalized form and strips file endings for files of recognized programming languages.
function convertFilepath(filePath) {
    filePath = filePath.replace(/\/\/|\//g, '.') // convert all // and / to .
    filePath = filePath.replace(/\\\\|\\/g, '.') // convert all \\ and \ to .
    filePath = filePath.replace(/.java$/, '').replace(/.py$/, ''); // strip file endings for recognized nodes // TODO: Adjust for more languages.
    return filePath;
}


class GraphNode {
    constructor(filePath, lineNumber, isOldLineHighlighted) {
        this.filePath = filePath;
        this.lineNumber = lineNumber;

        let convertedFilepath = convertFilepath(filePath);

        let nodesInFile = getNodes().filter(n => convertedFilepath == convertFilepath(n.filePath));
        let candidateNodes = nodesInFile.filter(n => this._positionMatches(n, lineNumber, isOldLineHighlighted));

        if (nodesInFile.length > 0 && candidateNodes == 0) {
            this.node = nodesInFile.find(n => n.type == NodeType.SCRIPT);
            return;
        }
        else if (candidateNodes.length == 0) {
            this.node = getNodes().find(n => filePath.endsWith(n.name));
            return;
        }

        this.maxLineNumber = Math.max(...candidateNodes.map(n => this._position(n, isOldLineHighlighted)[0]));
        candidateNodes = candidateNodes.filter(n => this._position(n, isOldLineHighlighted)[0] == this.maxLineNumber);

        this.node = candidateNodes[0];

        if (candidateNodes.length > 1) {
            if (isOldLineHighlighted) {
                this.node = candidateNodes.find(n => n.status == NodeStatus.DELETED);
            }
            else {
                this.node = candidateNodes.find(n => n.status == NodeStatus.ADDED);
            }
        }
    }

    matches = (lineNumber, isOldLine) => {
        var candidateNodesNew = [];
        if (this.classNodes.length != 0) {
            candidateNodesNew = this.classNodes.filter(n => this._positionMatches(n, lineNumber, isOldLine));
        }
        if (candidateNodesNew.length == 0) {
            if (this.node == getNodes().find(n => this.filePath.endsWith(n.id.replace(/\//g, '.')))) {
                return true;
            }
            return false;
        }
        if (this.node == undefined) { return false; }
        var maxLineNumberNew = Math.max(...candidateNodesNew.map(n => this._position(n, isOldLine)[0]));
        var nodeNew = candidateNodesNew.find(n => this._position(n, isOldLine)[0] == maxLineNumberNew);
        return nodeNew.id == this.node.id;
    }

    _position = (node, isOldLine) => {
        return isOldLine && node.positionOld != null && node.positionOld.length == 2 ? node.positionOld : node.position;
    }

    _positionMatches = (node, lineNumber, isOldLine) => {
        var position = this._position(node, isOldLine);
        return position[0] <= lineNumber && position[1] >= lineNumber;
    }
}


// Adds comment indicators for changed lines.
function addCommentIndicators() {

    let diffDiscussions = Array.from(document.getElementsByClassName("diff-grid-comments"));
    let reviewDiscussions = new Map(); // key: id, value: ordered (by line) list of discussions
    let perNodeDiscussionLineNumbers = new Map(); // key: id, value: ordered list of lines with discussions

    diffDiscussions.forEach(diffDiscussion => {
        let commentedLine = diffDiscussion.previousElementSibling;

        if (commentedLine.classList.contains('line_holder')) {
            let node = getNodeFromLine(commentedLine);

            if (node) {
                let discussions = getDiscussions(diffDiscussion);

                if (!reviewDiscussions.has(node.node.id)) {
                    discussions = [discussions]; // add nesting to differentiate by line
                    reviewDiscussions.set(node.node.id, discussions);
                    perNodeDiscussionLineNumbers.set(node.node.id, [node.lineNumber]);
                }
                else {
                    let previousDiscussions = reviewDiscussions.get(node.node.id);
                    previousDiscussions.push(discussions);
                    perNodeDiscussionLineNumbers.get(node.node.id).push(node.lineNumber);
                }
            }
        }
    });

    if (reviewDiscussions.size > 0) {
        languageSpecificElements.get('graphs')
            .forEach(graph => graph.addCommentIndicators(perNodeDiscussionLineNumbers, reviewDiscussions));
    }
}


// Returns list of discussions, each discussion consisting of a list of comments.
function getDiscussions (diffComments) {
    let discussions = [];
    let diffDiscussionElements = Array.from(diffComments.getElementsByClassName('diff-discussions'));

    diffDiscussionElements.forEach(discussion => {
        let commentThread = [];
        let commentElements = Array.from(discussion.getElementsByClassName('note-text'));

        commentElements.forEach(commentElement => {
            commentThread.push(commentElement.children[0].textContent);
        });

        discussions.push(commentThread);
    });

    return discussions;
}


function getNodeFromLine (lineHolder) {

    let lineContent = lineHolder.children[0].querySelector(':scope > .line_content');
    if (lineContent == undefined) {
        lineContent = lineHolder.children[0].querySelector(':scope > .diff-line-num');
    }

    if (lineContent == undefined) {
        return;
    }

    let isOldLine = lineContent.classList.contains('old');

    if (isOldLine) {
        var line = lineHolder.getElementsByClassName('old_line')[0];
    }
    else {
        var line = lineHolder.getElementsByClassName('new_line')[1];
    }

    try {
        var lineNumberLink = line.getElementsByTagName('a')[0];
    }
    catch (TypeError) {
        // Line not changed (neither old nor new).
        return;
    }

    let fileHolder = lineHolder.closest('.file-holder');
    var filePath = fileHolder.getElementsByClassName("file-title-name")[0].attributes['data-original-title'];
    filePath = filePath == undefined ? fileHolder.getElementsByClassName("file-title-name")[0].attributes['title'] : filePath;

    if (lineNumberLink == undefined || filePath == undefined) {
        return; // no link found
    }

    let lineNumber = lineNumberLink.attributes['data-linenumber'].value;
    filePath = filePath.value.replace(' deleted', '');
    
    return new GraphNode(filePath, lineNumber, isOldLine);
}


function mouseOverCode (event) {
    if (languageSpecificElements.get('graphs').size == 0) {
        return;
    }

    var lineHolder = event.toElement.closest('.line_holder');
    if (lineHolder != undefined) {
        if (event.toElement.classList.contains('empty-cell')) {
            return; // empty cell hovered
        }
        var containsDefinition = event.toElement.classList.contains('line_content') || event.toElement.classList.contains('diff-line-num')
        var classes;
        if (containsDefinition) {
            classes = event.toElement.classList
        } else {
            var candidate = event.toElement.closest('.line_content');
            if (candidate == undefined) {
                candidate = event.toElement.closest('.diff-line-num');
            }
            if (candidate == null) {
                // error finding candidate
                return;
            }
            classes = candidate.classList;
        }

        const isOldLine = classes.contains('old');

        if (isOldLine) {
            var line = lineHolder.getElementsByClassName('old_line')[0];
        }
        else {
            var line = lineHolder.getElementsByClassName('new_line')[1];
        }

        try {
            var lineNumberLink = line.getElementsByTagName('a')[0];
        }
        catch (TypeError) {
            return;
        }

        var filePath = event.currentTarget.getElementsByClassName("file-title-name")[0].attributes['data-original-title'];
        filePath = filePath == undefined ? event.currentTarget.getElementsByClassName("file-title-name")[0].attributes['title'] : filePath;

        if (lineNumberLink == undefined || filePath == undefined) {
            return; // no link found
        }
        const lineNumber = lineNumberLink.attributes['data-linenumber'].value;
        filePath = filePath.value.replace(' deleted', '');

        if (highlightedNode != undefined && highlightedNode.classNodePath == convertFilepath(filePath) && highlightedNode.matches(lineNumber, isOldLine)) { // TODO: Adjust for other languages.
            return; // same highlight
        }

        languageSpecificElements.get('graphs').forEach(graph => {
            graph._onHoverExit();
            graph._tick();
        });

        highlightedNode = new GraphNode(filePath, lineNumber, isOldLine);

        if (highlightedNode.node != undefined) {
            languageSpecificElements.get('windows').forEach((graphWindow, language) => {
                d3.select(graphWindow.document.body).selectAll('g.node')
                    .filter(n => n.id == highlightedNode.node.id)
                    .each(n => {
                        let graph = languageSpecificElements.get('graphs').get(language);
                        graph.focus(n);
                        graph._onNodeHover(n);
                    });
            });
        }
    }
}

function mouseLeaveCode (event) {
    if (languageSpecificElements.get('graphs').size == 0) {
        return;
    }
    highlightedNode = undefined;
    languageSpecificElements.get('graphs').forEach(graph => {
        graph._onHoverExit();
        graph._tick();
    });
}

function getClickableElement (filePath, lineNumber) {
    if (filePath == null) {
        return null;
    }
    var filePath = filePath.split('\\').join('/');
    const fileElement = Array.prototype.find.call(
        document.getElementsByClassName("file-title-name"),
        fileTitle => {
            var title = fileTitle.attributes["data-original-title"];
            title = title == undefined ? fileTitle.attributes['title'] : title;
            return title != undefined && filePath.endsWith(title.value.replace(' deleted', ''));
        });
    if (fileElement == undefined) {
        return null;
    }
    return getCorrespondingLineNumber(fileElement, lineNumber);
}

function getCorrespondingLineNumber (fileElement, lineNumber) {
    if (lineNumber == null) {
        return fileElement.closest('.file-header-content').getElementsByTagName('a')[0];
    }
    var clickableElement = Array.prototype.flatMap.call(
        fileElement.closest(".diff-file").getElementsByClassName("diff-line-num"),
        line => Array.prototype.filter.call(
            line.getElementsByTagName("a"),
            lineNumberLink => lineNumber == lineNumberLink.attributes["data-linenumber"].value
        )
    ).find(element => element != undefined);
    if (clickableElement != undefined) {
        return clickableElement;
    }
    return fileElement.parentElement;
}

isClickable = e => {
    return e != null && ((e.getAttribute('onclick') != null) || (e.getAttribute('href') != null));
}
