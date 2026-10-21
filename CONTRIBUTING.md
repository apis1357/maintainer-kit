# Contributing

Thanks for contributing.

## Development

Maintainer Kit requires Python 3.9+ and has no runtime dependencies.

Run tests:

```bash
python -m unittest discover -s tests -v
```

Run the audit against this repository:

```bash
python -m maintainer_kit .
```

## Pull requests

Keep changes focused. Include tests for behavior changes. Explain operational or compatibility impact in the pull-request template.

## Scope

The project intentionally avoids network access and provider-specific API dependencies in its core audit engine.
