# b-thesis-botschen

This is the backend component of ReviewVis, used to analyze changesets and create the graph. The graph can be exported to a file to use for the frontend.



## Requirements

The tool requires Python (version > 3.5) and jedi to be installed on the machine. Jedi (and its dependencies) can be installed automatically when using the tool for the first time.


## Usage

To use the tool, the branches that should be compared have to be present on your local machine.
The guide is written for bash (defining variables, using git diff), but the tools can be used on Linux or Windows.

The process works by first creating a list of changed files. This list is then used as input for CDP, which analyzes the project and creates the graph.

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

Use codediffparser (and save output into json file):
```bash script
py -m codediffparser --source ${gitlabSourceBranch} --target ${gitlabTargetBranch} --changed path/to/changed_files.json > out.json
```


## Examples and Tests

There are some tests defined, which also showcase different situations. The output (stored in ./test/results) can also be used as example and guide for how the output should look.
The tests aren't up-to-date (the node names have changed) but the underlying structure (types and number of nodes and relations) are still correct and can be used as a guideline together with the thesis.

Tests can be executed as follows: py -m unittest test.<testname>