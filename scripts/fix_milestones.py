#!/usr/bin/env python3
"""Audit and fix GitHub Issue milestone assignments.

Reads all docs/*.md story files, determines the correct milestone for each,
fetches current GitHub milestones, and fixes any mismatches.

Usage:
    uv run python scripts/fix_milestones.py
"""

import json
import re
import subprocess
from pathlib import Path

from _milestones import CAPABILITY_NORMALIZE, MILESTONE_TITLES, correct_milestone_key

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"


def gh(*args: str) -> str:
    result = subprocess.run(
        ["gh", *args], capture_output=True, text=True, encoding="utf-8", check=True
    )
    return result.stdout.strip()


def main() -> None:
    # Fetch all current issue milestones (open + closed)
    print("Fetching current GitHub issue milestones...")
    # Use URL query params (not --field) for GET requests; output JSON objects to avoid
    # jq string-interpolation escaping issues when passed through Python + subprocess.
    raw = gh(
        "api",
        "--paginate",
        "repos/:owner/:repo/issues?state=all&per_page=100",
        "--jq",
        ".[] | {n: .number, m: .milestone.title}",
    )
    issue_milestone: dict[int, str] = {}
    for line in raw.splitlines():
        line = line.strip()
        if not line:
            continue
        obj: dict[str, object] = json.loads(line)
        issue_milestone[int(str(obj["n"]))] = str(obj["m"]) if obj["m"] is not None else "none"

    fixes: list[dict[str, object]] = []

    for path in sorted(DOCS.glob("*.md")):
        content = path.read_text(encoding="utf-8")

        issue_m = re.search(r"^\*\*GitHub Issue:\*\* #(\d+)", content, re.MULTILINE)
        if not issue_m:
            continue
        issue_num = int(issue_m.group(1))

        title_m = re.search(r"^# (.+)$", content, re.MULTILINE)
        title = title_m.group(1) if title_m else path.stem

        cap_m = re.search(r"^\*\*Capability:\*\* (.+)$", content, re.MULTILINE)
        cap_raw = cap_m.group(1).strip() if cap_m else "infrastructure"
        capability = CAPABILITY_NORMALIZE.get(cap_raw.lower(), "infrastructure")

        correct_key = correct_milestone_key(content, capability)
        correct_title = MILESTONE_TITLES.get(correct_key, "")
        current_title = issue_milestone.get(issue_num, "none")

        if current_title != correct_title:
            fixes.append(
                {
                    "issue": issue_num,
                    "title": title,
                    "file": path.name,
                    "current": current_title,
                    "correct": correct_title,
                }
            )

    if not fixes:
        print("All milestones are correct. Nothing to fix.")
        return

    print(f"\nFound {len(fixes)} mismatch(es):\n")
    for fix in fixes:
        print(f"  #{fix['issue']} {fix['title']}")
        print(f"    File:    {fix['file']}")
        print(f"    Current: {fix['current']}")
        print(f"    Correct: {fix['correct'] or '(no milestone)'}")

    print("\nApplying fixes...")
    for fix in fixes:
        issue_str = str(fix["issue"])
        correct = fix["correct"]
        if correct:
            gh("issue", "edit", issue_str, "--milestone", str(correct))
        else:
            # Clear milestone via REST API
            gh(
                "api",
                f"repos/:owner/:repo/issues/{issue_str}",
                "--method",
                "PATCH",
                "--field",
                "milestone=null",
            )
        label = str(correct) if correct else "(no milestone)"
        print(f"  ✓ #{fix['issue']} → {label}")

    print("\nDone.")


if __name__ == "__main__":
    main()
