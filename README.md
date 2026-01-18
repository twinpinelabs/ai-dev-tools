# git-aiblame

A Python CLI tool that extends `git blame` with AI attribution detection. Shows which lines of code were written by humans versus AI assistants by parsing commit message patterns.

## Why This Tool?

As AI coding assistants become standard in development workflows, teams need visibility into how their codebase is being shaped. Most AI assistants add signatures to commits (e.g., "Co-Authored-By: Claude"), but `git blame` doesn't surface this information in a useful way.

`git-aiblame` solves this by:

1. **Quick attribution check** - See at a glance which lines came from AI assistants
2. **No setup required** - Works with existing commit conventions, no tracking infrastructure needed
3. **Complements Source Trace** - Lightweight CLI companion to Twin Pine Labs' analytics product
4. **Audit-friendly** - Useful for teams that need to understand AI contribution levels

## License

MIT
