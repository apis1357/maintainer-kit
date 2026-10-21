from __future__ import annotations

import argparse
import json
from pathlib import Path

from .audit import audit_repository, as_jsonable, score


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="maintainer-kit",
        description="Audit repository readiness for sustainable OSS maintenance.",
    )
    p.add_argument("path", nargs="?", default=".", help="Repository path (default: .)")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--min-score", type=int, default=0,
                   help="Exit with status 1 when score is below this value.")
    return p


def render_markdown(checks) -> str:
    value = score(checks)
    lines = [
        "# Maintainer Kit report",
        "",
        f"**Score: {value}/100**",
        "",
        "| Status | Check | Points | Evidence |",
        "|---|---|---:|---|",
    ]
    for c in checks:
        status = "PASS" if c.passed else "FAIL"
        points = c.weight if c.passed else 0
        lines.append(f"| {status} | {c.title} | {points}/{c.weight} | {c.evidence} |")
    failed = [c for c in checks if not c.passed]
    if failed:
        lines += ["", "## Remediation", ""]
        for c in failed:
            lines.append(f"- **{c.title}:** {c.remediation}")
    return "\n".join(lines)


def main(argv=None) -> int:
    args = _parser().parse_args(argv)
    root = Path(args.path)
    if not root.exists() or not root.is_dir():
        print(f"error: repository path does not exist or is not a directory: {root}")
        return 2

    checks = audit_repository(root)
    value = score(checks)

    if args.format == "json":
        print(json.dumps(as_jsonable(checks), indent=2))
    else:
        print(render_markdown(checks))

    return 1 if value < args.min_score else 0
