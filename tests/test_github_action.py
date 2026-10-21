import tempfile
import unittest
from pathlib import Path

from maintainer_kit.github_action import write_github_files


class GitHubActionTests(unittest.TestCase):
    def test_writes_summary_and_outputs(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            summary = root / "summary.md"
            output = root / "output.txt"
            write_github_files(
                "# Report\n\nOK",
                91,
                True,
                {"GITHUB_STEP_SUMMARY": str(summary), "GITHUB_OUTPUT": str(output)},
            )
            self.assertEqual(summary.read_text(encoding="utf-8"), "# Report\n\nOK\n")
            self.assertEqual(output.read_text(encoding="utf-8"), "score=91\npassed=true\n")

    def test_missing_github_paths_is_a_noop(self):
        write_github_files("report", 50, False, {})


if __name__ == "__main__":
    unittest.main()
