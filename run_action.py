from pathlib import Path
import subprocess
import sys

minimum = sys.argv[1] if len(sys.argv) > 1 else "80"
cmd = [
    sys.executable,
    str(Path(__file__).parent / "standalone.py"),
    ".",
    "--min-score",
    minimum,
]
raise SystemExit(subprocess.call(cmd))
