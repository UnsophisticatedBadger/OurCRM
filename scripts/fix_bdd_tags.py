#!/usr/bin/env python3
"""Fix BDD scenario tags in story docs to match each story's GitHub issue number.

During the story migration, story numbers changed. This script updates every
@story_OLD and @usNNN tag in each doc to @story_CORRECT based on the
**GitHub Issue:** #N field in that doc.

Safe to re-run — files that are already correct are not written.

Usage:
    uv run python scripts/fix_bdd_tags.py           # dry-run (preview only)
    uv run python scripts/fix_bdd_tags.py --apply   # write changes
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"


def fix_content(content: str, issue_num: str) -> str:
    correct = f"@story_{issue_num}"
    content = re.sub(r"@story_\d+", correct, content)
    content = re.sub(r"@us_?\d+", correct, content)
    return content


def main() -> None:
    apply = "--apply" in sys.argv

    paths = sorted(p for p in DOCS.glob("*.md") if re.match(r"^\d+", p.name))
    changed: list[tuple[str, list[str]]] = []

    for path in paths:
        content = path.read_text(encoding="utf-8-sig")

        if re.search(r"^\*\*Status:\*\*\s+Done", content, re.MULTILINE):
            continue

        issue_m = re.search(r"^\*\*GitHub Issue:\*\* #(\d+)", content, re.MULTILINE)
        if not issue_m:
            continue

        issue_num = issue_m.group(1)
        new_content = fix_content(content, issue_num)

        if new_content == content:
            continue

        wrong = sorted(
            {*re.findall(r"@story_(\d+)", content), *re.findall(r"@us_?\d+", content)}
            - {f"story_{issue_num}"}
        )
        changed.append((path.name, wrong))

        if apply:
            path.write_text(new_content, encoding="utf-8")

    if not changed:
        print("All BDD tags are correct.")
        return

    verb = "Fixed" if apply else "Would fix"
    for name, old_tags in changed:
        print(f"  {verb}: {name}  [{', '.join(old_tags)}]")

    print(f"\n{verb} {len(changed)} files.")
    if not apply:
        print("\nRe-run with --apply to write changes.")


if __name__ == "__main__":
    main()
