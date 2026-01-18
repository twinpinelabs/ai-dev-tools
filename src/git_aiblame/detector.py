"""AI attribution detection from commit messages."""

import re
from typing import Optional

from .config import AI_PATTERNS


class AIDetector:
    """Detects AI involvement in commits."""

    def __init__(self, patterns: Optional[dict] = None):
        """Initialize detector with optional custom patterns."""
        self.patterns = patterns or AI_PATTERNS
        self.compiled_patterns = {
            ai_type: [re.compile(pattern) for pattern in pattern_list]
            for ai_type, pattern_list in self.patterns.items()
        }

    def detect(self, commit_message: str) -> Optional[str]:
        """Detect AI type from commit message.

        Args:
            commit_message: Full commit message

        Returns:
            AI type name (e.g., "claude", "copilot") or None if not detected
        """
        for ai_type, compiled_list in self.compiled_patterns.items():
            for pattern in compiled_list:
                if pattern.search(commit_message):
                    return ai_type
        return None

    def is_ai_assisted(self, commit_message: str) -> bool:
        """Check if commit shows any AI assistance."""
        return self.detect(commit_message) is not None

    def parse_commit_message(self, commit_message: str) -> dict:
        """Parse commit message and extract AI attribution info.

        Args:
            commit_message: Full commit message

        Returns:
            Dict with 'ai_type' and 'is_ai' keys
        """
        ai_type = self.detect(commit_message)
        return {
            "ai_type": ai_type,
            "is_ai": ai_type is not None,
        }
