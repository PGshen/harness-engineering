"""Tests for templates/scripts/check_docs.py. Run: python3 -m unittest discover tests"""

from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
SCRIPT = SKILL / "templates" / "scripts" / "check_docs.py"


def load_module():
    spec = importlib.util.spec_from_file_location("check_docs", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CheckDocsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.mod = load_module()
        self.mod.ROOT = self.root
        (self.root / "docs" / "decisions").mkdir(parents=True)
        (self.root / "docs" / "SOP.md").write_text("# SOP\n", encoding="utf-8")
        (self.root / "docs" / "decisions" / "0001-采用流程.md").write_text(
            "# 0001\n\n## 元信息\n\n## 背景\n\n## 决定\n\n## 考虑过的其他方案\n\n## 影响\n", encoding="utf-8"
        )
        (self.root / "AGENTS.md").write_text("# AGENTS\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write(self, rel: str, text: str) -> Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def links(self, rel: str, text: str) -> list[str]:
        path = self.write(rel, text)
        return self.mod.check_links(path, text)

    def test_relative_link_ok_and_missing(self) -> None:
        self.assertEqual(self.links("docs/a.md", "[s](SOP.md)"), [])
        self.assertEqual(len(self.links("docs/a.md", "[s](nope.md)")), 1)

    def test_url_encoded_link(self) -> None:
        text = "[d](decisions/0001-%E9%87%87%E7%94%A8%E6%B5%81%E7%A8%8B.md)"
        self.assertEqual(self.links("docs/a.md", text), [])

    def test_repo_root_link(self) -> None:
        self.assertEqual(self.links("docs/decisions/x.md", "[s](/docs/SOP.md)"), [])
        self.assertEqual(len(self.links("docs/decisions/x.md", "[s](/docs/nope.md)")), 1)

    def test_anchor_external_and_code_ignored(self) -> None:
        text = "[a](#x) [b](https://example.com) `[c](nope.md)`\n```\n[d](nope.md)\n```\n[e](SOP.md#part)"
        self.assertEqual(self.links("docs/a.md", text), [])

    def test_plan_missing_sections(self) -> None:
        self.write("docs/plans/active/m1-x.md", "# m1\n\n## 元信息\n")
        self.assertEqual(self.mod.main(), 1)

    def test_adr_duplicate_number_and_bad_name(self) -> None:
        self.write("docs/decisions/0001-另一个.md", (self.root / "docs/decisions/0001-采用流程.md").read_text())
        self.write("docs/decisions/bad.md", "# bad\n")
        self.assertEqual(self.mod.main(), 1)

    def test_tech_debt_ids(self) -> None:
        check = self.mod.check_tech_debt_ids
        path = self.write("docs/quality/tech-debt.md", "")
        ok = "| TD-1 | x |\n| TD-2 | y |\n## 已处理\n| TD-3 | z |\n| TD-1（部分） | w |\n"
        self.assertEqual(check(path, ok), [])
        self.assertEqual(len(check(path, "| TD-1 | x |\n|TD-1| y |\n")), 1)
        self.assertEqual(len(check(path, "| TD-1 | x |\n## 已处理\n| TD-1 | z |\n")), 1)

    def test_agents_line_limit(self) -> None:
        self.write("AGENTS.md", "x\n" * (self.mod.AGENTS_MAX_LINES + 1))
        self.assertEqual(self.mod.main(), 1)

    def test_clean_tree_passes(self) -> None:
        self.assertEqual(self.mod.main(), 0)

    def test_git_ignored_files_skipped(self) -> None:
        try:
            subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        except (OSError, subprocess.CalledProcessError):
            self.skipTest("git not available")
        self.write(".gitignore", "data/\n")
        self.write("data/evidence/notes.md", "[x](missing.md)")
        self.assertEqual(self.mod.main(), 0)
        self.write("docs/b.md", "[x](missing.md)")
        self.assertEqual(self.mod.main(), 1)


if __name__ == "__main__":
    unittest.main()
