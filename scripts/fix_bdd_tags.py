#!/usr/bin/env python3
"""One-time fix: convert bare @NNN BDD tags to @story_NNN.

Numeric-only pytest marks are not valid Python identifiers and cause
PytestUnknownMarkWarning. This script converts them to the @story_NNN
format without making any GitHub API calls.

Usage:
    uv run python scripts/fix_bdd_tags.py
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TESTS_BDD = ROOT / "tests" / "bdd"
CLAUDE_MD = ROOT / "CLAUDE.md"

# Matches a bare @NNN tag — digits only after @, not already prefixed with story_
BARE_TAG = re.compile(r"@(\d+)\b")


def fix_bare_tags(content: str) -> str:
    return BARE_TAG.sub(lambda m: f"@story_{m.group(1)}", content)


def process(path: Path) -> bool:
    content = path.read_text(encoding="utf-8")
    updated = fix_bare_tags(content)
    if updated != content:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0

    print("Fixing story docs...")
    for path in sorted(DOCS.glob("*.md")):
        if process(path):
            print(f"  ✓ {path.name}")
            changed += 1

    bdd_files = sorted(
        list(TESTS_BDD.glob("features/*.feature")) + list(TESTS_BDD.glob("test_*.py"))
    )
    if bdd_files:
        print("\nFixing BDD files...")
        for path in bdd_files:
            if process(path):
                print(f"  ✓ {path.relative_to(ROOT)}")
                changed += 1

    print("\nFixing CLAUDE.md...")
    content = CLAUDE_MD.read_text(encoding="utf-8")
    updated = fix_bare_tags(content)
    # Also update the pytest command example
    updated = re.sub(
        r'`uv run pytest -m "(\d+)"`',
        lambda m: f'`uv run pytest -m "story_{m.group(1)}"`',
        updated,
    )
    if updated != content:
        CLAUDE_MD.write_text(updated, encoding="utf-8")
        print("  ✓ CLAUDE.md")
        changed += 1
    else:
        print("  ~ CLAUDE.md (unchanged)")

    print(f"\nDone. {changed} file(s) updated.")


if __name__ == "__main__":
    main()
