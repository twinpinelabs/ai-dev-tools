"""Enable python -m git_aiblame invocation."""

from .cli import main

if __name__ == "__main__":
    import sys

    sys.exit(main())
