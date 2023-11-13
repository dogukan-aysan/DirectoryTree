"""This module provides the application’s command-line interface."""

from argparse import ArgumentParser, SUPPRESS
import pathlib
import sys

from model import TreeGenerator
from __init__ import __version__


def main():
    args = parse_command_line_arguments()
    given_path = pathlib.Path(args.path)
    if not given_path.is_dir():
        print("This not a valid path")
        sys.exit()
    if args.dir_only and args.file_only:
        print("Only one should be included (dir_only | file_only)")
        sys.exit()
    else:
        tree_generator = TreeGenerator(
            args.path,
            args.depth,
            args.colorless,
            args.hidden,
            args.dir_only,
            args.file_only,
        )
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
        help="set the maximum allowed depth (default: 5, max: 10)",
        metavar="<num>",
    )
    # colorless tree
    detailed.add_argument(
        "--colorless",
        action="store_true",
        default=False,
        help="generate colorless tree (default: false)",
    )
    # hidden
    detailed.add_argument(
        "--hidden",
        action="store_true",
        default=False,
        help="include hidden items (default: false)",
    )
    # dir_only
    detailed.add_argument(
        "--dir_only",
        action="store_true",
        default=False,
        help="include directories only (default: false)",
    )
    # file_only
    detailed.add_argument(
        "--file_only",
        action="store_true",
        default=False,
        help="include files only (default: false)",
    )
    # version
    detailed.add_argument(
        "-v", action="version", version=f"directory_tree v{__version__}"
    )

    return parser.parse_args()
