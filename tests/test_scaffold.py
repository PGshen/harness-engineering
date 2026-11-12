"""End-to-end test: scaffold into a fresh repo, then the generated docs check passes.

Run: python3 -m unittest discover tests
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
SCAFFOLD = SKILL / "scripts" / "scaffold.py"


def run(*args: str, cwd: Path, env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(list(args), cwd=cwd, capture_output=True, text=True, env=env)


class ScaffoldTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name).resolve()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def scaffold(self, *extra: str) -> subprocess.CompletedProcess:
        return run(sys.executable, str(SCAFFOLD), str(self.repo), "--name", "demo", *extra, cwd=self.repo)

    def test_dry_run_writes_nothing(self) -> None:
        result = self.scaffold("--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(list(self.repo.iterdir()), [])

    def test_scaffold_creates_files_and_substitutes(self) -> None:
        self.assertEqual(self.scaffold().returncode, 0)
        self.assertTrue((self.repo / ".githooks" / "pre-commit").stat().st_mode & 0o111)
        self.assertIn("demo", (self.repo / "AGENTS.md").read_text(encoding="utf-8"))
        for path in self.repo.rglob("*"):
            if path.is_file():
                self.assertNotIn("{{", path.read_text(encoding="utf-8", errors="ignore"), path)

    def test_never_overwrites(self) -> None:
        (self.repo / "AGENTS.md").write_text("mine\n", encoding="utf-8")
        result = self.scaffold()
        self.assertIn("= AGENTS.md", result.stdout)
        self.assertEqual((self.repo / "AGENTS.md").read_text(encoding="utf-8"), "mine\n")

    def test_generated_docs_check_passes(self) -> None:
        self.scaffold()
        result = run(sys.executable, "scripts/check_docs.py", cwd=self.repo)
        self.assertEqual(result.returncode, 0, result.stdout)

    @unittest.skipUnless(shutil.which("make") and shutil.which("git"), "make and git required")
    def test_make_check_warns_and_strict_fails(self) -> None:
        run("git", "init", "-q", ".", cwd=self.repo)
        self.scaffold()
        env = {**os.environ, "PYTHON": sys.executable}
        loose = run("make", "check", cwd=self.repo, env=env)
        self.assertEqual(loose.returncode, 0, loose.stdout + loose.stderr)
        self.assertIn("警告", loose.stderr)
        strict = run("make", "check", "STRICT=1", cwd=self.repo, env=env)
        self.assertNotEqual(strict.returncode, 0)


if __name__ == "__main__":
    unittest.main()
