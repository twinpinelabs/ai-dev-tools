"""Git blame integration and line attribution."""

import subprocess
from dataclasses import dataclass
from typing import List, Optional


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
