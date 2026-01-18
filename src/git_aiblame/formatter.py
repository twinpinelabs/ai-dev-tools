"""Output formatting for git-aiblame."""

import sys
from typing import List

from .blame import BlameLine

ANSI_COLORS = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "cyan": "\033[36m",
}

COLOR_ENABLED = sys.stdout.isatty()


def colorize(text: str, color: str) -> str:
    """Add ANSI color codes to text if color is enabled.

    Args:
        text: Text to colorize
        color: Color name from ANSI_COLORS

    Returns:
        Colorized text
    """
    if not COLOR_ENABLED:
        return text
    return f"{ANSI_COLORS.get(color, '')}{text}{ANSI_COLORS['reset']}"


def format_plain(blame_lines: List[BlameLine]) -> str:
    """Format blame output as plain text.

    Args:
        blame_lines: List of BlameLine objects

    Returns:
        Formatted plain text output
    """
    lines = []
    for bl in blame_lines:
        lines.append(
            f"{bl.line_number:4d} | {bl.commit_hash[:7]} | {bl.author:12} | {bl.content}"
        )
    return "\n".join(lines)


def format_colored(blame_lines: List[BlameLine]) -> str:
    """Format blame output with ANSI colors.

    Args:
        blame_lines: List of BlameLine objects

    Returns:
        Formatted colored output
    """
    lines = []
    for bl in blame_lines:
        line_str = (
            f"{colorize(str(bl.line_number).rjust(4), 'cyan')} | "
            f"{colorize(bl.commit_hash[:7], 'blue')} | "
            f"{colorize(bl.author.ljust(12), 'yellow')} | "
            f"{bl.content}"
        )
        lines.append(line_str)
    return "\n".join(lines)
