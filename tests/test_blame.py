"""Tests for blame parsing and line attribution."""

import pytest

from git_aiblame.blame import BlameLine, parse_blame_output
from git_aiblame.detector import AIDetector


@pytest.fixture
def detector():
    """Create a detector instance."""
    return AIDetector()


class TestBlameLine:
    """Test BlameLine dataclass."""

    def test_blame_line_creation(self):
        """Test creating a BlameLine object."""
        bl = BlameLine(
            line_number=10,
            commit_hash="abc123def",
            author="John Doe",
            content="print('hello')",
        )
        assert bl.line_number == 10
        assert bl.commit_hash == "abc123def"
        assert bl.author == "John Doe"
        assert bl.content == "print('hello')"


class TestParseBlameOutput:
    """Test git blame output parsing."""

    def test_parse_empty_output(self, detector):
        """Test parsing empty output."""
        result = parse_blame_output("", detector)
        assert result == []

    def test_parse_simple_output(self, detector):
        """Test parsing simple blame output."""
        output = """abc123def456 (John Doe 2025-01-15 10:00:00 +0000 1)\tprint('hello')
def456abc789 (Jane Doe 2025-01-16 11:00:00 +0000 2)\tprint('world')
"""
        result = parse_blame_output(output, detector)
        assert len(result) == 2
        assert result[0].line_number == 1
        assert result[0].commit_hash == "abc123def456"
        assert result[0].content == "print('hello')"
        assert result[1].line_number == 2
        assert result[1].content == "print('world')"

    def test_parse_multiline_content(self, detector):
        """Test parsing with multiline content."""
        output = """abc123def456 (John Doe 2025-01-15 10:00:00 +0000 1)\tdef hello():
abc123def456 (John Doe 2025-01-15 10:00:00 +0000 2)\t    return 'world'
"""
        result = parse_blame_output(output, detector)
        assert len(result) == 2
        assert result[0].content == "def hello():"
        assert result[1].content == "    return 'world'"
