"""Standalone entrypoint for GitHub Action usage without installation."""
import sys
from maintainer_kit.cli import main

raise SystemExit(main(sys.argv[1:]))
