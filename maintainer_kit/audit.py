from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Iterable

from .config import Policy, PolicyError


@dataclass(frozen=True)
class Check:
    key: str
    title: str
    weight: int
    passed: bool
    evidence: str
    remediation: str


CANDIDATES = {
    "readme": ["README.md", "README.rst", "README.txt", "README"],
    "license": ["LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"],
    "contributing": ["CONTRIBUTING.md", ".github/CONTRIBUTING.md"],
    "security": ["SECURITY.md", ".github/SECURITY.md"],
    "conduct": ["CODE_OF_CONDUCT.md", ".github/CODE_OF_CONDUCT.md"],
    "pr_template": [
        ".github/pull_request_template.md",
        ".github/PULL_REQUEST_TEMPLATE.md",
        "PULL_REQUEST_TEMPLATE.md",
    ],
    "agents": ["AGENTS.md", ".github/AGENTS.md"],
}


def _first_existing(root: Path, candidates: Iterable[str]) -> Path | None:
    for candidate in candidates:
        p = root / candidate
        if p.is_file():
            return p
    return None


def _has_any_file(root: Path, directory: str) -> bool:
    p = root / directory
    return p.is_dir() and any(x.is_file() for x in p.rglob("*"))


def _exists_glob(root: Path, patterns: Iterable[str]) -> Path | None:
    for pattern in patterns:
        for p in root.glob(pattern):
            if p.is_file():
                return p
    return None


def _apply_policy(checks: list[Check], policy: Policy) -> list[Check]:
    known = {check.key for check in checks}
    unknown_disabled = sorted(set(policy.disabled_checks) - known)
    unknown_weights = sorted(set(policy.weights or {}) - known)
    unknown = unknown_disabled + [key for key in unknown_weights if key not in unknown_disabled]
    if unknown:
        raise PolicyError(f"unknown check keys in policy: {', '.join(unknown)}")

    configured: list[Check] = []
    for check in checks:
        if check.key in policy.disabled_checks:
            continue
        configured.append(replace(check, weight=policy.weight_for(check.key, check.weight)))
    return configured


def audit_repository(root: Path, policy: Policy | None = None) -> list[Check]:
    root = root.resolve()

    def file_check(key, title, weight, candidates, remediation):
        found = _first_existing(root, candidates)
        return Check(
            key, title, weight, bool(found),
            str(found.relative_to(root)) if found else "not found",
            remediation,
        )

    checks = [
        file_check("readme", "README", 12, CANDIDATES["readme"],
                   "Add a README describing purpose, installation, usage, and support."),
        file_check("license", "License", 12, CANDIDATES["license"],
                   "Add an OSI-approved license file."),
        file_check("security", "Security policy", 10, CANDIDATES["security"],
                   "Add SECURITY.md with a private vulnerability reporting path."),
        file_check("contributing", "Contributing guide", 8, CANDIDATES["contributing"],
                   "Add CONTRIBUTING.md with setup, test, and review expectations."),
        file_check("conduct", "Code of conduct", 5, CANDIDATES["conduct"],
                   "Add a concise code of conduct and enforcement contact."),
        file_check("pr_template", "Pull-request template", 6, CANDIDATES["pr_template"],
                   "Add .github/pull_request_template.md."),
        file_check("agents", "Agent instructions", 6, CANDIDATES["agents"],
                   "Add AGENTS.md with repository-local validation and contribution rules."),
    ]

    ci = _exists_glob(root, [".github/workflows/*.yml", ".github/workflows/*.yaml"])
    checks.append(Check(
        "ci", "Continuous integration", 12, bool(ci),
        str(ci.relative_to(root)) if ci else "not found",
        "Add a GitHub Actions workflow that runs tests and validation.",
    ))

    issue_templates = _has_any_file(root, ".github/ISSUE_TEMPLATE")
    checks.append(Check(
        "issue_templates", "Issue templates", 6, issue_templates,
        ".github/ISSUE_TEMPLATE" if issue_templates else "not found",
        "Add structured bug/feature issue templates.",
    ))

    dep = _exists_glob(root, [
        ".github/dependabot.yml",
        ".github/renovate.json",
        "renovate.json",
        "renovate.json5",
    ])
    checks.append(Check(
        "dependency_automation", "Dependency automation", 7, bool(dep),
        str(dep.relative_to(root)) if dep else "not found",
        "Configure Dependabot or Renovate.",
    ))

    tests = any((root / p).is_dir() for p in ["tests", "test", "__tests__"])
    checks.append(Check(
        "tests", "Tests", 9, tests,
        "tests directory found" if tests else "not found",
        "Add automated tests under tests/ (or another conventional test directory).",
    ))

    release = _exists_glob(root, [
        ".github/workflows/*release*.yml",
        ".github/workflows/*release*.yaml",
        ".github/workflows/*publish*.yml",
        ".github/workflows/*publish*.yaml",
    ])
    checks.append(Check(
        "release", "Release automation", 7, bool(release),
        str(release.relative_to(root)) if release else "not found",
        "Add a reproducible release/publish workflow when releases are applicable.",
    ))

    return _apply_policy(checks, policy) if policy else checks


def score(checks: list[Check]) -> int:
    total = sum(c.weight for c in checks)
    earned = sum(c.weight for c in checks if c.passed)
    return round(100 * earned / total) if total else 0


def as_jsonable(checks: list[Check]) -> dict:
    return {
        "score": score(checks),
        "checks": [asdict(c) for c in checks],
    }
