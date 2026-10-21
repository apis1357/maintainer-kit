from __future__ import annotations

import os
from pathlib import Path
from typing import Mapping


def write_github_files(report: str, score_value: int, passed: bool, env: Mapping[str, str] | None = None) -> None:
    environment = os.environ if env is None else env

    summary_path = environment.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with Path(summary_path).open("a", encoding="utf-8") as handle:
            handle.write(report.rstrip() + "\n")

    output_path = environment.get("GITHUB_OUTPUT")
    if output_path:
        with Path(output_path).open("a", encoding="utf-8") as handle:
            handle.write(f"score={score_value}\n")
            handle.write(f"passed={'true' if passed else 'false'}\n")
