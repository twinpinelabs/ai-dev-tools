"""Output formatting for git-aiblame."""

from typing import List

from .blame import BlameLine


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
