# Maintainer Kit

[![CI](https://github.com/apis1357/maintainer-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/apis1357/maintainer-kit/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/apis1357/maintainer-kit)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](pyproject.toml)

A small, dependency-free CLI and GitHub Action that audits whether a repository is ready for sustainable open-source maintenance.

It checks for operational files and workflows that maintainers commonly need: licensing, contribution guidance, security reporting, CI, issue and pull-request templates, dependency updates, tests, releases, and agent instructions.

## Why

Open-source maintenance is more than code. A project also needs predictable contribution, review, security, and release workflows.

Maintainer Kit turns those expectations into a repeatable repository check that can run locally or in CI.

## Features

- Zero runtime dependencies
- Markdown and JSON reports
- Exit-code threshold for CI
- Repository-local policy configuration
- GitHub Actions job summary plus `score` and `passed` outputs
- Weighted checks for README, licensing, security, contribution guidance, CI, templates, dependency automation, tests, releases, and `AGENTS.md`
- Clear remediation guidance for failed checks

## Installation

Install the current development version directly from GitHub:

```bash
python -m pip install "git+https://github.com/apis1357/maintainer-kit.git"
```

After `v0.1.0` is published, pin production use to that release:

```bash
python -m pip install "git+https://github.com/apis1357/maintainer-kit.git@v0.1.0"
```

For contributor development:

```bash
git clone https://github.com/apis1357/maintainer-kit.git
cd maintainer-kit
python -m pip install -e .
```

## Quick start

```bash
maintainer-kit .
```

The module entry point is equivalent:

```bash
python -m maintainer_kit .
```

JSON output:

```bash
maintainer-kit . --format json
```

Fail CI if the score is below 80:

```bash
maintainer-kit . --min-score 80
```

## Repository policy

Add `.maintainer-kit.json` to customize the audit without forking the tool:

```json
{
  "minimum_score": 80,
  "disabled_checks": ["release"],
  "weights": {
    "security": 15,
    "tests": 12
  }
}
```

Supported fields are documented in [`docs/policy.md`](docs/policy.md). CLI `--min-score` takes precedence over `minimum_score` from repository policy.

## GitHub Action

```yaml
name: Maintainer readiness

on:
  pull_request:
  push:
    branches: [main]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - id: maintainer
        uses: apis1357/maintainer-kit@v0.1.0
        with:
          min-score: "80"
      - run: echo "score=${{ steps.maintainer.outputs.score }} passed=${{ steps.maintainer.outputs.passed }}"
```

The Action also writes the Markdown audit report to the GitHub Actions job summary.

For production use, pin the action to a release tag or commit SHA.

## Scoring

Each enabled check carries a weight based on its operational importance. The final score is normalized to 100.

A high score does not guarantee project quality or security. It indicates that important maintenance surfaces are present and discoverable.

## Design principles

- Prefer transparent repository-local policy over hidden configuration.
- Keep checks deterministic and inspectable.
- Avoid network calls by default.
- Never claim that a file's presence proves process quality.
- Make remediation explicit.

## Development

```bash
python -m unittest discover -s tests -v
python -m maintainer_kit . --min-score 80
```

## License

Apache-2.0.
