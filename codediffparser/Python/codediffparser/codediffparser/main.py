from .parser import Parser
from .mode import Mode

from argparse import ArgumentParser


def main(cli_args=None):
    """Entrypoint for module."""

    usage = """py -m codediffparser --source sourceBranch --target targetBrancht --changed changed.json"""
    desc = "Execute codediffparser to extract the call and dependency graph."

    arg_parser = ArgumentParser(usage=usage, description=desc)
    arg_parser.add_argument("--source", help="path to source branch")
    arg_parser.add_argument("--target", help="path to target branch")
    arg_parser.add_argument("--changed", help="path to changed_files.json")


    known_args, _ = arg_parser.parse_known_args(cli_args)

    if known_args.source is None:
        print("Missing argument: source")
        return
    
    if known_args.target is None:
        print("Missing argument: target")
        return

    if known_args.changed is None:
        print("Missing argument: changed")
        return


    with open(known_args.changed) as changed_files_list:
        filter_files = [f for f in changed_files_list.read().split("\n") if f]
    
    source_branch = known_args.source
    target_branch = known_args.target

    parser = Parser()
    parser.parse(target_branch, filter_files, Mode.TARGET)
    parser.parse(source_branch, filter_files, Mode.SOURCE)

    print(parser.get_result())