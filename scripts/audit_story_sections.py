#!/usr/bin/env python3
"""Audit story docs for required sections and metadata fields.

Checks every docs/NNN-*.md file and reports which required
sections or header fields are missing.

Usage:
    uv run python scripts/audit_story_sections.py
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

REQUIRED_SECTIONS = [
    "## User Story",
    "## Dependencies",
    "## Acceptance Criteria",
    "## Test Locations",
    "## Definition of Done",
]

REQUIRED_FIELDS = [
    r"\*\*Capability:\*\*",
    r"\*\*Milestone:\*\*",
    r"\*\*Status:\*\*",
    r"\*\*GitHub Issue:\*\*",
]

FIELD_LABELS = [
    "**Capability:**",
    "**Milestone:**",
    "**Status:**",
    "**GitHub Issue:**",
]


def audit(path: Path) -> list[str]:
    content = path.read_text(encoding="utf-8-sig")
    issues = []

    for section in REQUIRED_SECTIONS:
        if section not in content:
            issues.append(f"missing section: {section}")

    for pattern, label in zip(REQUIRED_FIELDS, FIELD_LABELS, strict=True):
        if not re.search(pattern, content, re.MULTILINE):
            issues.append(f"missing field: {label}")

    # Check Test Locations section has an actual table
    if "## Test Locations" in content:
        tl_match = re.search(r"## Test Locations\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
        if tl_match and "|" not in tl_match.group(1):
            issues.append("Test Locations section has no table")

    return issues


def main() -> None:
    # Only audit numbered story docs, skip definition-of-ready etc.
    paths = sorted(p for p in DOCS.glob("*.md") if re.match(r"^\d+", p.name))

    clean = 0
    skipped = 0
    dirty: list[tuple[str, list[str]]] = []

    for path in paths:
        content = path.read_text(encoding="utf-8-sig")

        # Skip Done stories — they're complete and won't be worked on
        if re.search(r"^\*\*Status:\*\*\s+Done", content, re.MULTILINE):
            skipped += 1
            continue

        issues = audit(path)
        if issues:
            dirty.append((path.name, issues))
        else:
            clean += 1

    active = len(paths) - skipped
    print(f"Audited {active} active story docs ({skipped} Done stories skipped)\n")

    if not dirty:
        print("All docs are complete.")
        return

    # Group by missing item for a summary view
    section_counts: dict[str, int] = {}
    field_counts: dict[str, int] = {}
    for _, issues in dirty:
        for issue in issues:
            if issue.startswith("missing section"):
                section_counts[issue] = section_counts.get(issue, 0) + 1
            else:
                field_counts[issue] = field_counts.get(issue, 0) + 1

    print("=== Summary ===")
    for label, count in sorted(section_counts.items(), key=lambda x: -x[1]):
        print(f"  {count:3d}  {label}")
    for label, count in sorted(field_counts.items(), key=lambda x: -x[1]):
        print(f"  {count:3d}  {label}")

    print(f"\n=== Detail ({len(dirty)} docs with gaps) ===")
    for name, issues in dirty:
        print(f"\n  {name}")
        for issue in issues:
            print(f"    - {issue}")

    print(f"\n{clean} complete, {len(dirty)} with gaps, {skipped} Done stories skipped.")


if __name__ == "__main__":
    main()
