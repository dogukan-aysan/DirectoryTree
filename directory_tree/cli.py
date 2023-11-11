"""This module provides the application’s command-line interface."""

from argparse import ArgumentParser, SUPPRESS

from model import TreeGenerator
from __init__ import __version__
import pathlib
import sys


def main():
    args = parse_command_line_arguments()
    given_path = pathlib.Path(args.path)
    if not given_path.is_dir():
        print("This not a valid path")
        sys.exit()
    else:
        tree_generator = TreeGenerator(args.path, args.depth, args.colorless)
        tree = tree_generator.generate()
        print(tree)


def parse_command_line_arguments():
    parser = ArgumentParser(
        prog="directory_tree",
        description="generate and display a tree-like diagram listing the internal structure of a given root directory",
        epilog="thanks for using %(prog)s! :)",
        argument_default=SUPPRESS,
    )
    general = parser.add_argument_group("general output")
    # path
    general.add_argument(
        "path",
        nargs="?",
        default=".",
        help="set given path as root directory (default: %(default)s)",
    )
    detailed = parser.add_argument_group("detailed output")
    # depth
    detailed.add_argument(
        "--depth",
        type=int,
        default=5,
        choices=range(1, 11),
        help="set the maximum allowed depth",
        metavar="<num>",
    )
    # colorless tree
    detailed.add_argument(
        "--colorless",
        action="store_true",
        default=False,
        help="allow colorless tree",
    )
    # version
    detailed.add_argument(
        "-v", action="version", version=f"directory_tree v{__version__}"
    )

    return parser.parse_args()
