#!/usr/bin/env python3
"""Sync GitHub issue bodies with current docs/*.md content.

The story docs were edited after issues were created, so issue bodies are
stale. This script updates issue bodies to match their doc files.

Usage:
    uv run python scripts/sync_issue_bodies.py          # sync every story doc
    uv run python scripts/sync_issue_bodies.py 3         # sync only issue #3
"""

import argparse
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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "issue",
        nargs="?",
        type=int,
        default=None,
        help="Only sync this GitHub issue number (default: sync all story docs)",
    )
    args = parser.parse_args()

    paths = sorted(DOCS.glob("*.md"))
    updated = 0
    failed = 0
    matched = 0

    if args.issue is not None:
        print(f"Syncing story doc for issue #{args.issue} to its GitHub issue body...\n")
    else:
        print(f"Syncing {len(paths)} story docs to GitHub issue bodies...\n")

    for path in paths:
        # Strip BOM if present (some editors save UTF-8 with BOM on Windows)
        content = path.read_text(encoding="utf-8-sig")

        issue_m = re.search(r"^\*\*GitHub Issue:\*\* #(\d+)", content, re.MULTILINE)
        if not issue_m:
            if args.issue is None:
                print(f"  ⚠  No GitHub Issue field: {path.name}")
            continue
        issue_num = int(issue_m.group(1))
        if args.issue is not None and issue_num != args.issue:
            continue
        matched += 1

        # Write to a temp file to avoid Windows command-line length limits
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", suffix=".md", delete=False
            ) as tmp:
                tmp.write(content)
                tmp_path = tmp.name
            gh("issue", "edit", str(issue_num), "--body-file", tmp_path)
            print(f"  ✓ #{issue_num} {path.name}")
            updated += 1
        except subprocess.CalledProcessError as e:
            print(f"  ✗ #{issue_num} {path.name}: {e.stderr.strip()}")
            failed += 1
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    if args.issue is not None and matched == 0:
        print(f"No story doc found with GitHub Issue #{args.issue}")
        return

    print(f"\nDone. {updated} updated, {failed} failed.")


if __name__ == "__main__":
    main()
