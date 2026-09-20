from importlib.machinery import SourceFileLoader
import importlib.util
import os
import sys
import unittest

script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "merge-dependabot"))
loader = SourceFileLoader("merge_dependabot", script_path)
spec = importlib.util.spec_from_loader("merge_dependabot", loader)
md = importlib.util.module_from_spec(spec)
loader.exec_module(md)


class TestMergeDependabot(unittest.TestCase):
    def test_parse_github_nwo(self):
        self.assertEqual(
            md.parse_github_nwo("https://github.com/SiavoshZarrasvand/screenplays.git"),
            "SiavoshZarrasvand/screenplays"
        )
        self.assertEqual(
            md.parse_github_nwo("git@github.com:SiavoshZarrasvand/homebrew-purgeapp.git"),
            "SiavoshZarrasvand/homebrew-purgeapp"
        )
        self.assertEqual(
            md.parse_github_nwo("https://github.com/SiavoshZarrasvand/cv"),
            "SiavoshZarrasvand/cv"
        )

    def test_evaluate_ci_empty(self):
        # Without require_ci
        is_green, reason = md.evaluate_ci([], require_ci=False)
        self.assertTrue(is_green)
        self.assertIn("assumed clean", reason)

        # With require_ci
        is_green, reason = md.evaluate_ci([], require_ci=True)
        self.assertFalse(is_green)
        self.assertIn("No CI checks found", reason)

    def test_evaluate_ci_passed(self):
        checks = [
            {"__typename": "CheckRun", "name": "Build", "status": "COMPLETED", "conclusion": "SUCCESS"},
            {"__typename": "CheckRun", "name": "Test", "status": "COMPLETED", "conclusion": "SKIPPED"},
            {"__typename": "StatusContext", "context": "ci/lint", "state": "SUCCESS"},
        ]
        is_green, reason = md.evaluate_ci(checks, require_ci=True)
        self.assertTrue(is_green)
        self.assertIn("All 3 checks passed", reason)

    def test_evaluate_ci_failure(self):
        checks = [
            {"__typename": "CheckRun", "name": "Cloudflare Pages", "status": "COMPLETED", "conclusion": "FAILURE"},
        ]
        is_green, reason = md.evaluate_ci(checks, require_ci=False)
        self.assertFalse(is_green)
        self.assertIn("Failed checks: Cloudflare Pages (FAILURE)", reason)

    def test_evaluate_ci_pending(self):
        checks = [
            {"__typename": "CheckRun", "name": "E2E", "status": "IN_PROGRESS", "conclusion": ""},
        ]
        is_green, reason = md.evaluate_ci(checks, require_ci=False)
        self.assertFalse(is_green)
        self.assertIn("in progress or queued", reason)


if __name__ == "__main__":
    unittest.main()
