#!/usr/bin/env python3
"""Copy the harness templates into a target repository without overwriting anything.

Usage:
  python3 scaffold.py <target-dir> --name <project-name> [--dry-run]

- Files that already exist are skipped and listed, so they can be merged by hand.
- {{PROJECT_NAME}} and {{DATE}} placeholders are substituted.
- templates/githooks/ is installed as .githooks/ (enable with `make setup`).
"""

from __future__ import annotations

import argparse
import datetime as dt
import shutil
import stat
import sys
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parent.parent / "templates"
RENAMES = {"githooks": ".githooks"}
TEXT_SUFFIXES = {".md", ".py", ".sh", ""}
# Local junk that must never be copied into a target repository.
IGNORED_NAMES = {".DS_Store", "Thumbs.db"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}
IGNORED_DIRS = {"__pycache__"}


def destination(src: Path, target: Path) -> Path:
    parts = list(src.relative_to(TEMPLATES).parts)
    parts[0] = RENAMES.get(parts[0], parts[0])
    return target.joinpath(*parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("target", type=Path)
    parser.add_argument("--name", required=True, help="project name used in templates")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    target = args.target.resolve()
    if not target.is_dir():
        print(f"目标目录不存在：{target}", file=sys.stderr)
        return 2

    today = dt.date.today().isoformat()
    created, skipped = [], []
    for src in sorted(p for p in TEMPLATES.rglob("*") if p.is_file()):
        rel_parts = src.relative_to(TEMPLATES).parts
        if src.name in IGNORED_NAMES or src.suffix in IGNORED_SUFFIXES or any(p in IGNORED_DIRS for p in rel_parts):
            continue
        dst = destination(src, target)
        shown = dst.relative_to(target)
        if dst.exists():
            skipped.append(shown)
            continue
        created.append(shown)
        if args.dry_run:
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.suffix in TEXT_SUFFIXES:
            text = src.read_text(encoding="utf-8")
            text = text.replace("{{PROJECT_NAME}}", args.name).replace("{{DATE}}", today)
            dst.write_text(text, encoding="utf-8")
            shutil.copymode(src, dst)
        else:
            shutil.copy2(src, dst)
        if dst.parent.name == ".githooks" or dst.suffix in (".py", ".sh"):
            dst.chmod(dst.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    verb = "将创建" if args.dry_run else "已创建"
    print(f"{verb} {len(created)} 个文件：")
    for p in created:
        print(f"  + {p}")
    if skipped:
        print(f"已存在、跳过 {len(skipped)} 个文件（需要手工合并，见 references/retrofit.md）：")
        for p in skipped:
            print(f"  = {p}")
    if not args.dry_run:
        print("下一步：改 Makefile 的 check-code / check-fast-code，填 AGENTS.md，然后 make setup && make check（填完用 make check STRICT=1 确认没有遗漏的占位）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
