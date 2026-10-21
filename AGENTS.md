# AGENTS.md

## Goal

Maintain a small, deterministic, dependency-free repository auditing tool.

## Invariants

- Core audits must not make network requests.
- Audits must not execute files from the target repository.
- A check must be deterministic for the same filesystem state.
- New checks require tests and explicit remediation text.
- Do not claim that file presence proves security or process quality.

## Validation

Run:

```bash
python -m unittest discover -s tests -v
python -m maintainer_kit .
```

## Change policy

Prefer focused changes. Avoid adding dependencies unless they provide concrete, measured value.
