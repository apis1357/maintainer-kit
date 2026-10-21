# Repository policy

Maintainer Kit can read an optional `.maintainer-kit.json` file from the repository root.

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

## Fields

- `minimum_score`: integer from 0 to 100. Used when `--min-score` is not supplied.
- `disabled_checks`: array of check keys to omit from scoring.
- `weights`: object mapping check keys to positive integer weights.

Unknown top-level keys and malformed values are rejected with an actionable error. The configuration is data only; it is never executed as code.
