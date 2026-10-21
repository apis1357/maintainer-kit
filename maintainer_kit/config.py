from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


CONFIG_NAME = ".maintainer-kit.json"


class PolicyError(ValueError):
    """Raised when repository policy configuration is invalid."""


@dataclass(frozen=True)
class Policy:
    minimum_score: int = 0
    disabled_checks: frozenset[str] = frozenset()
    weights: dict[str, int] | None = None

    def weight_for(self, key: str, default: int) -> int:
        if not self.weights:
            return default
        return self.weights.get(key, default)


def _validate_score(value: object) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 100:
        raise PolicyError("minimum_score must be an integer between 0 and 100")
    return value


def load_policy(root: Path) -> Policy:
    path = root / CONFIG_NAME
    if not path.exists():
        return Policy()

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PolicyError(f"invalid {CONFIG_NAME}: {exc}") from exc

    if not isinstance(data, dict):
        raise PolicyError(f"{CONFIG_NAME} must contain a JSON object")

    allowed = {"minimum_score", "disabled_checks", "weights"}
    unknown = sorted(set(data) - allowed)
    if unknown:
        raise PolicyError(f"unknown policy keys: {', '.join(unknown)}")

    minimum_score = _validate_score(data.get("minimum_score", 0))

    disabled = data.get("disabled_checks", [])
    if not isinstance(disabled, list) or any(not isinstance(item, str) or not item for item in disabled):
        raise PolicyError("disabled_checks must be an array of non-empty strings")

    raw_weights = data.get("weights", {})
    if not isinstance(raw_weights, dict):
        raise PolicyError("weights must be an object mapping check keys to positive integers")
    weights: dict[str, int] = {}
    for key, value in raw_weights.items():
        if not isinstance(key, str) or not key:
            raise PolicyError("weight keys must be non-empty strings")
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise PolicyError(f"weight for {key!r} must be a positive integer")
        weights[key] = value

    return Policy(
        minimum_score=minimum_score,
        disabled_checks=frozenset(disabled),
        weights=weights,
    )
