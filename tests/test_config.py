import json
import tempfile
import unittest
from pathlib import Path

from maintainer_kit.audit import audit_repository
from maintainer_kit.config import PolicyError, load_policy


class PolicyTests(unittest.TestCase):
    def test_defaults_when_config_is_missing(self):
        with tempfile.TemporaryDirectory() as d:
            policy = load_policy(Path(d))
            self.assertEqual(policy.minimum_score, 0)
            self.assertEqual(policy.disabled_checks, frozenset())

    def test_overrides_and_disabled_checks(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "README.md").write_text("x", encoding="utf-8")
            (root / ".maintainer-kit.json").write_text(
                json.dumps({
                    "minimum_score": 75,
                    "disabled_checks": ["release"],
                    "weights": {"readme": 20},
                }),
                encoding="utf-8",
            )
            policy = load_policy(root)
            checks = {c.key: c for c in audit_repository(root, policy)}
            self.assertEqual(policy.minimum_score, 75)
            self.assertEqual(checks["readme"].weight, 20)
            self.assertNotIn("release", checks)

    def test_malformed_config_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / ".maintainer-kit.json").write_text("{bad json", encoding="utf-8")
            with self.assertRaises(PolicyError):
                load_policy(root)

    def test_unknown_check_key_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / ".maintainer-kit.json").write_text(
                json.dumps({"disabled_checks": ["does-not-exist"]}),
                encoding="utf-8",
            )
            policy = load_policy(root)
            with self.assertRaises(PolicyError):
                audit_repository(root, policy)


if __name__ == "__main__":
    unittest.main()
