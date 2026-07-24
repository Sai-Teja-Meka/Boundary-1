"""`python3 -m shell.dogfood` — the DOGFOOD CLI entry point."""

import sys

from shell.dogfood.cli import main

if __name__ == "__main__":
    sys.exit(main())
