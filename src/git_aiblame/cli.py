"""Command-line interface for git-aiblame."""

import argparse
import sys

from .blame import get_line_attribution
from .formatter import format_plain, format_colored


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for git-aiblame.

    Returns:
        Configured ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        description="Git blame with AI attribution detection",
        prog="git-aiblame",
    )

    parser.add_argument("file", help="File to analyze with git blame")

    parser.add_argument(
        "-L",
        "--line-range",
        type=str,
        help="Line range in format START,END (e.g., -L 10,50)",
    )

    parser.add_argument(
        "--no-color", action="store_true", help="Disable colored output"
    )

    parser.add_argument("--stats", action="store_true", help="Show summary statistics")

    return parser
