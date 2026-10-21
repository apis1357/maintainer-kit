# Maintainer Kit

A small, dependency-free CLI and GitHub Action that audits whether a repository is ready for sustainable open-source maintenance.

It checks for operational files and workflows that maintainers commonly need: licensing, contribution guidance, security reporting, CI, issue and pull-request templates, dependency updates, tests, releases, and agent instructions.

## Why

Open-source maintenance is more than code. A project also needs predictable contribution, review, security, and release workflows.

Maintainer Kit turns those expectations into a repeatable repository check that can run locally or in CI.

## Features

- Zero runtime dependencies
- Markdown and JSON reports
- Exit-code threshold for CI
- Weighted checks for README, licensing, security, contribution guidance, CI, templates, dependency automation, tests, releases, and `AGENTS.md`
- Clear remediation guidance for failed checks

## Quick start

```bash
python -m maintainer_kit .
```

JSON output:

```bash
python -m maintainer_kit . --format json
```

Fail CI if the score is below 80:

```bash
python -m maintainer_kit . --min-score 80
```

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
      - uses: actions/checkout@v4
      - uses: apis1357/maintainer-kit@main
        with:
          min-score: "80"
```

For production use, pin the action to a release tag or commit SHA.

## Scoring

Each check carries a weight based on its operational importance. The final score is normalized to 100.

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
```

## License

Apache-2.0.
