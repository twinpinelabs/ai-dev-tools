"""Git blame integration and line attribution."""

import subprocess
from dataclasses import dataclass
from typing import Dict, List, Optional

from .detector import AIDetector


@dataclass
class BlameLine:
    """Represents a single line from git blame output."""

    line_number: int
    commit_hash: str
    author: str
    content: str


def run_git_blame(file_path: str, line_range: Optional[tuple] = None) -> str:
    """Run git blame command and return raw output.

    Args:
        file_path: Path to file to blame
        line_range: Optional tuple (start, end) for line range

    Returns:
        Raw git blame output string

    Raises:
        subprocess.CalledProcessError: If git blame fails
    """
    cmd = ["git", "blame", "--line-porcelain", file_path]

    if line_range:
        cmd.extend(["-L", f"{line_range[0]},{line_range[1]}"])

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)

    return result.stdout


def get_commit_message(commit_hash: str) -> str:
    """Get commit message for a given commit hash.

    Args:
        commit_hash: Git commit hash

    Returns:
        Commit message string
    """
    result = subprocess.run(
        ["git", "log", "-1", "--format=%B", commit_hash],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def parse_blame_output(output: str, detector: AIDetector) -> List[BlameLine]:
    """Parse git blame output and determine AI attribution.

    Args:
        output: Raw git blame --line-porcelain output
        detector: AIDetector instance for AI detection

    Returns:
        List of BlameLine objects with attribution
    """
    lines = []
    line_number = 1
    commit_hash = ""
    author = ""
    i = 0

    while i < len(output):
        line = output[i]

        if line.startswith(("author ", "author-time ", "author-mail ")):
            i += 1
            continue

        if line.startswith("\t"):
            content = line[1:].rstrip("\n")
            lines.append(
                BlameLine(
                    line_number=line_number,
                    commit_hash=commit_hash,
                    author=author,
                    content=content,
                )
            )
            line_number += 1
            i += 1
            continue

        if line[:40].isalnum() or len(line.split()[0]) == 40:
            commit_hash = line.split()[0]
            i += 1

            while i < len(output):
                next_line = output[i]
                if next_line.startswith("author "):
                    author = next_line[7:].rstrip("\n")
                elif next_line.startswith("\t"):
                    break
                i += 1
        else:
            i += 1

    return lines


def get_line_attribution(
    file_path: str, line_range: Optional[tuple] = None
) -> List[BlameLine]:
    """Get line attribution for a file with AI detection.

    Args:
        file_path: Path to file to analyze
        line_range: Optional tuple (start, end) for line range

    Returns:
        List of BlameLine objects
    """
    detector = AIDetector()
    raw_output = run_git_blame(file_path, line_range)
    return parse_blame_output(raw_output, detector)
