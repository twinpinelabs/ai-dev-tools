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


def main() -> int:
    """Main entry point for git-aiblame CLI.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = create_parser()
    args = parser.parse_args()

    line_range = None
    if args.line_range:
        try:
            start, end = args.line_range.split(",")
            line_range = (int(start), int(end))
        except ValueError:
            print("Error: Line range must be in format START,END", file=sys.stderr)
            return 1

    try:
        blame_lines = get_line_attribution(args.file, line_range)

        if args.stats:
            print_stats(args.file, blame_lines)
        else:
            if args.no_color:
                print(format_plain(blame_lines))
            else:
                print(format_colored(blame_lines))

        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def print_stats(file_path: str, blame_lines: list) -> None:
    """Print summary statistics for a file.

    Args:
        file_path: Path to the file
        blame_lines: List of BlameLine objects
    """
    total = len(blame_lines)
    print(f"File: {file_path}")
    print(f"Total lines: {total}")

    if total == 0:
        return

    human_count = 0
    ai_count = 0
    ai_types = {}

    for bl in blame_lines:
        ai_type = getattr(bl, "ai_type", None)
        if ai_type:
            ai_count += 1
            ai_types[ai_type] = ai_types.get(ai_type, 0) + 1
        else:
            human_count += 1

    human_pct = (human_count / total) * 100
    ai_pct = (ai_count / total) * 100

    print(f"Human: {human_count} ({human_pct:.0f}%)")
    print(f"AI-assisted: {ai_count} ({ai_pct:.0f}%)")

    if ai_types:
        for ai_type, count in sorted(ai_types.items(), key=lambda x: -x[1]):
            print(f"  - {ai_type.capitalize()}: {count} lines")
