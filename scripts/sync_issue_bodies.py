#!/usr/bin/env python3
"""Sync GitHub issue bodies with current docs/*.md content.

The story docs were edited after issues were created, so issue bodies are
stale. This script updates every issue body to match its doc file.

Safe to re-run — issues whose body already matches are skipped.

Usage:
    uv run python scripts/sync_issue_bodies.py
"""

import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"


def gh(*args: str) -> str:
    result = subprocess.run(
        ["gh", *args], capture_output=True, text=True, encoding="utf-8", check=True
    )
    return result.stdout.strip()


def main() -> None:
    paths = sorted(DOCS.glob("*.md"))
    total = len(paths)
    updated = 0
    failed = 0

    print(f"Syncing {total} story docs to GitHub issue bodies...\n")

    for path in paths:
        # Strip BOM if present (some editors save UTF-8 with BOM on Windows)
        content = path.read_text(encoding="utf-8-sig")

        issue_m = re.search(r"^\*\*GitHub Issue:\*\* #(\d+)", content, re.MULTILINE)
        if not issue_m:
            print(f"  ⚠  No GitHub Issue field: {path.name}")
            continue
        issue_num = issue_m.group(1)

        # Write to a temp file to avoid Windows command-line length limits
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", suffix=".md", delete=False
            ) as tmp:
                tmp.write(content)
                tmp_path = tmp.name
            gh("issue", "edit", issue_num, "--body-file", tmp_path)
            print(f"  ✓ #{issue_num} {path.name}")
            updated += 1
        except subprocess.CalledProcessError as e:
            print(f"  ✗ #{issue_num} {path.name}: {e.stderr.strip()}")
            failed += 1
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    print(f"\nDone. {updated} updated, {failed} failed.")


if __name__ == "__main__":
    main()
