#!/usr/bin/env python3
"""Strip the version prefix from every story doc's **Milestone:** field.

Milestone titles are capability names only now (e.g. "Secure Shell", not
"v0.2.0 — Secure Shell") — semantic-release auto-increments the version per
commit, so a version number can't be reliably pre-assigned to a milestone.

Safe to re-run — docs already in the new format are left unchanged.

Usage:
    uv run python scripts/fix_milestone_field.py           # dry-run (preview only)
    uv run python scripts/fix_milestone_field.py --apply   # write changes
"""

import re
import sys
from pathlib import Path

from _milestones import CAPABILITY_NORMALIZE, MILESTONE_TITLES, correct_milestone_key

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"


def main() -> None:
    apply = "--apply" in sys.argv
    changed: list[tuple[str, str, str]] = []

    for path in sorted(DOCS.glob("*.md")):
        content = path.read_text(encoding="utf-8-sig")

        ms_m = re.search(r"^\*\*Milestone:\*\* (.+)$", content, re.MULTILINE)
        if not ms_m:
            continue
        current = ms_m.group(1).strip()

        cap_m = re.search(r"^\*\*Capability:\*\* (.+)$", content, re.MULTILINE)
        cap_raw = cap_m.group(1).strip() if cap_m else "infrastructure"
        capability = CAPABILITY_NORMALIZE.get(cap_raw.lower(), "infrastructure")

        key = correct_milestone_key(content, capability)
        correct = MILESTONE_TITLES.get(key, current)

        if current == correct:
            continue

        changed.append((path.name, current, correct))

        if apply:
            new_content = re.sub(
                r"^\*\*Milestone:\*\* .+$",
                f"**Milestone:** {correct}",
                content,
                count=1,
                flags=re.MULTILINE,
            )
            path.write_text(new_content, encoding="utf-8")

    if not changed:
        print("All Milestone fields are already up to date.")
        return

    verb = "Fixed" if apply else "Would fix"
    for name, old, new in changed:
        print(f"  {verb}: {name}  [{old!r} → {new!r}]")

    print(f"\n{verb} {len(changed)} files.")
    if not apply:
        print("\nRe-run with --apply to write changes.")


if __name__ == "__main__":
    main()
