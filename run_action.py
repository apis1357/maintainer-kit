from pathlib import Path
import sys

from maintainer_kit.audit import audit_repository, score
from maintainer_kit.cli import render_markdown
from maintainer_kit.config import PolicyError, load_policy
from maintainer_kit.github_action import write_github_files


def main() -> int:
    try:
        minimum = int(sys.argv[1]) if len(sys.argv) > 1 else 80
    except ValueError:
        print("error: min-score must be an integer")
        return 2

    if not 0 <= minimum <= 100:
        print("error: min-score must be between 0 and 100")
        return 2

    root = Path(".")
    try:
        policy = load_policy(root)
        checks = audit_repository(root, policy)
    except PolicyError as exc:
        print(f"error: {exc}")
        return 2

    value = score(checks)
    passed = value >= minimum
    report = render_markdown(checks)
    print(report)
    write_github_files(report, value, passed)
    return 0 if passed else 1


raise SystemExit(main())
