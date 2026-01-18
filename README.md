# git-aiblame

A Python CLI tool that extends `git blame` with AI attribution detection. Shows which lines of code were written by humans versus AI assistants by parsing commit message patterns.

## Why This Tool?

As AI coding assistants become standard in development workflows, teams need visibility into how their codebase is being shaped. Most AI assistants add signatures to commits (e.g., "Co-Authored-By: Claude"), but `git blame` doesn't surface this information in a useful way.

`git-aiblame` solves this by:

1. **Quick attribution check** - See at a glance which lines came from AI assistants
2. **No setup required** - Works with existing commit conventions, no tracking infrastructure needed
3. **Complements Source Trace** - Lightweight CLI companion to Twin Pine Labs' analytics product
4. **Audit-friendly** - Useful for teams that need to understand AI contribution levels

## Installation

```bash
# Install from PyPI (when published)
pip install git-aiblame

# Or install from source
git clone https://github.com/twinpinelabs/ai-dev-tools.git
cd ai-dev-tools
pip install -e .
```

## Usage Examples

### Basic Usage

```bash
# Show blame with AI attribution
git-aiblame src/cli.py
```

Output:
```
   1 | abc123d | John Doe    | def hello():
   2 | def456a | Jane Smith  |     return 'world'
```

### Line Ranges

```bash
# Check specific line range
git-aiblame src/cli.py -L 10,50
```

### Plain Output

```bash
# Disable colored output
git-aiblame src/cli.py --no-color
```

### Statistics

```bash
# Show summary statistics
git-aiblame src/cli.py --stats
```

Output:
```
File: src/cli.py
Total lines: 142
Human: 98 (69%)
AI-assisted: 44 (31%)
  - Claude: 38 lines
  - Copilot: 6 lines
```

## License

MIT
