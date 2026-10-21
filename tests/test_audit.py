import tempfile
import unittest
from pathlib import Path

from maintainer_kit.audit import audit_repository, score


class AuditTests(unittest.TestCase):
    def test_empty_repository_scores_zero(self):
        with tempfile.TemporaryDirectory() as d:
            checks = audit_repository(Path(d))
            self.assertEqual(score(checks), 0)

    def test_core_files_are_detected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for name in ["README.md", "LICENSE", "SECURITY.md", "CONTRIBUTING.md", "AGENTS.md"]:
                (root / name).write_text("x", encoding="utf-8")
            checks = {c.key: c for c in audit_repository(root)}
            for key in ["readme", "license", "security", "contributing", "agents"]:
                self.assertTrue(checks[key].passed, key)

    def test_ci_threshold(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            wf = root / ".github" / "workflows"
            wf.mkdir(parents=True)
            (wf / "ci.yml").write_text("name: ci", encoding="utf-8")
            checks = {c.key: c for c in audit_repository(root)}
            self.assertTrue(checks["ci"].passed)


if __name__ == "__main__":
    unittest.main()
