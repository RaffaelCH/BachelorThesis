# b-thesis-botschen


This is the code for the tool ReviewVis. It analyzes all changed files contained in a review change-set, extracting code entities (i.e., classes, methods, functions, and script files if they contain procedural code) and their relationships (i.e. dependencies and method/function calls). Then, ReviewVis creates a call and dependency graph where the code entities are displayed as nodes, while links between nodes represent their connections or interactions (e.g., dependencies or method calls). The graph is displayed in a separate browser window (opened when visiting supported pages) at code review time. Currently it supports Java and Python programs and only works with GitLab.

More details can be found in the thesis.



### Structure

The program has two components: CodeDiffParser (CDP) and CodeDiffVis (CDV). CDP is the backend responsible for analyzing the code, and storing the results in a json file. CDV is the frontend which can visualize the output of CDP (or similar programs). They work independently of each other, meaning that the output of CDP needs to manually be moved to where CDV can access it (although that can be automated).


### Examples

If you just want to see how it works, there are examples provided in the files example_small.json, example_big.json and combined.json in the the codediffvis directory. The corresponding code is in the /examples directory and on Github [here](https://gitlab.com/RaffaelCH/cdv-examples). example_small.json is used for the [small merge request](https://gitlab.com/RaffaelCH/cdv-examples/-/merge_requests/1/diffs), example_big.json for the [large one](https://gitlab.com/RaffaelCH/cdv-examples/-/merge_requests/2/diffs), and combined.json showcases a combination of code in mutiple languages (Java and Python).
To see them, follow the Visualize the Changes subchapter. This is recommended to get a feel for how everything works.



### Analyze Projects

To use the tool, the branches that should be compared have to be present on your local machine and the languages that should be analyzed should be installed on your machine. The guide is written for bash (defining variables, using git diff), but the tools can be used in Linux or Windows.

The process works by first creating a list of changed files. This list is then used as input for CDP, which analyzes the project and creates the graph.
Each language currently needs its own parser, which can be found under /codediffparser/LANGUAGE. The output from this can then be used as input for CDV.

Define the branch names to be compared (source should be merged into target):
```bash script
gitlabSourceBranch=additions
gitlabTargetBranch=main
```

Download the branches to your local machine (can be skipped if already present):
```bash script
git clone --single-branch --branch ${gitlabSourceBranch} <your_gitlab_url> ${gitlabSourceBranch}
git clone --single-branch --branch ${gitlabTargetBranch} <your_gitlab_url> ${gitlabTargetBranch}
```

Get the changed files and output them to a file:
```bash script
git diff --name-only ${gitlabSourceBranch} ${gitlabTargetBranch} | grep -v ".git" | grep -E "${gitlabSourceBranch}|${gitlabTargetBranch}" | sed "s/^\($gitlabTargetBranch\|$gitlabSourceBranch\)//" > changed_files.json
```

Analyze Java project (jar is in /codediffparser/Java/codefiffparser/out/artifacts/codediffparser_jar):
```bash script
java -jar <path_to_jar> ${gitlabSourceBranch}/ ${gitlabTargetBranch}/ your_user_home/.m2/ changed_files.json > out.json
```

Analyze Python project (need to be in /codediffparser/Python/codediffparser directory):
```bash script
py -m codediffparser --source ${gitlabSourceBranch} --target ${gitlabTargetBranch} --changed path/to/changed_files.json > out.json
```

If you want to compare changes from multiple graphs (possibly including multiple languages) together, you can merge the jsons created using the commands above using the `json-combiner.py` Python tool.
```bash script
py json-combiner.py file_path_1.json [file_path_2.json [file_path_3.json [...]]] > combined_out.json
```


### Visualize the Changes

For now, only Google Chrome and Gitlab are supported.

In Chrome, go to chrome://extensions/ and enable the "developer mode" on the top right. Then, choose "load unpacked" on the top left, and select the codediffvis directory.
On the top right, click on the puzzle piece symbol to bring up the extensions, and pin the CDV extension. If you now visit a supported page (e.g. a merge request page), you should be able to see the colored CodeDiffVis (CDV) symbol. It will try to load the graph(s) whenever a supported page is loaded. When reloading the page, the graph(s) get also reloaded.

To use CDV for a graph, it needs to have access to the file containing it. To do this, copy the file (e.g. out.json) to the codediffvis directory from which you loaded the extension. Sometimes there is an issue where it doesn't have access. To test this, copy the file contents to a file in the same directory for which you have confirmed that it can be loaded.

Click on the codediffvis symbol to bring up the settings.
- Json Url: Can be set either relative to the location (directory) of the local codediffvis extension (e.g. out.json) or a web url.
- Change-based colors: Switch between change-based and package-based colors. The change-based coloring is as follows:
    - Red: Deleted (i.e., this node is only present in the target branch)
    - Green: New (i.e., this node is only present in the source branch)
    - Orange: Changed (i.e., within this node, there were changes (not counting commitments))
    - Grey: Java only - generated nodes that have the @Generated annotation
    - Light blue: Nodes not in supported languages (i.e., JavaScript, Properties, XML files, etc.)
- Hide nodes for unknown files: Hide or show nodes not written in any of the supported languages.
- Hide generated nodes: Java only - hide/show generated nodes that have the @Generated annotation.
- Hide methods: Hide or show the methods for OOP code.
- Hide warnings: Hide or show individual errors that ocurred in CDP when analyzing the program (tool errors, not code errors).
- One window per language: Open a separate window for each language or combine them into one window.

There exist the following types of nodes (differentiated by the identifier (letter before their name) and appearance):
- Script nodes (S): For statements not contained in any other node.
- Class nodes (C): For classes. If methods are shown, surrounded by colored circle.
- Abstract classes (A), Interfaces (I): For supported languages, specific types of classes with their own identifier.
- Method nodes: Can be toggled in settings, always connected to a class node.
- Functions (F): Functions in functional programming languages.
- Warning nodes: Dotted yellow border. When clicking on them, shows errors of CDP (e.g., could not resolve call). Not errors of the code itself.
They are connected with other nodes with different lines depending on if they are part of the node (e.g. method-class), or call it (e.g. function calls method).
If there are multiple languages in a window, each languages' nodes get a different colored border.

To improve the experience when using the tool, there are multiple possible interactions:
- Pan: Pan around the graph to show different parts by clicking and holding the background and moving the mouse.
- Drag: Nodes can be dragged around by clicking and holding a node and moving the mouse.
- Zoom: Zoom in or out of the graph using the mouse wheel.
- Hover: Hovering over a node highlights the connected nodes.
- Code-to-graph: Hovering over the code in Gitlab highlights the corresponding node in the graph.
- Graph-to-code: Clicking on a node jumps to the corresponding code in Gitlab.

Other information:
- The Gitlab window needs to be open for the graph to be interactive.
- Bug: Depending on the initial position of the nodes, some can float away (multiple nodes and forces interacting to push them group in one direction). Update the graph by dragging a node around to stop that.