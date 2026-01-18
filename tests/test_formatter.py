"""Tests for output formatting."""

import pytest

from git_aiblame.blame import BlameLine
from git_aiblame.formatter import format_plain, format_colored


@pytest.fixture
def blame_lines():
    """Create sample blame lines."""
    return [
        BlameLine(
            line_number=1,
            commit_hash="abc123def456",
            author="John Doe",
            content="def hello():",
        ),
        BlameLine(
            line_number=2,
            commit_hash="def456abc789",
            author="Jane Smith",
            content="    return 'world'",
        ),
    ]


class TestFormatPlain:
    """Test plain text formatting."""

    def test_format_plain_output(self, blame_lines):
        """Test plain text formatting."""
        result = format_plain(blame_lines)
        assert "   1 | abc123d | John Doe    | def hello():" in result
        assert "   2 | def456a | Jane Smith  |     return 'world'" in result

    def test_format_empty_list(self):
        """Test formatting empty list."""
        result = format_plain([])
        assert result == ""


class TestFormatColored:
    """Test colored output formatting."""

    def test_format_colored_output(self, blame_lines):
        """Test colored formatting."""
        result = format_colored(blame_lines)
        assert "abc123d" in result
        assert "John Doe" in result
        assert "def hello():" in result

    def test_format_empty_list(self):
        """Test colored formatting of empty list."""
        result = format_colored([])
        assert result == ""
