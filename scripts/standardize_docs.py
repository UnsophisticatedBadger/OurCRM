#!/usr/bin/env python3
"""Standardise story docs and GitHub issues after migration.

1. Rewrite H1 headings to "# NNN - Title" (first-letter title-cased per word)
2. Add or correct **Milestone:** field in every story doc
3. Update GitHub issue titles to match
4. Replace @us-NNN / @usNNN BDD tags with @NNN in story docs + feature files
5. Replace US-NNN references in story bodies (excluding Dependencies) with #N
6. Update @us-NNN examples in CLAUDE.md

Usage:
    uv run python scripts/standardize_docs.py
"""

from __future__ import annotations

import json
import re
import subprocess
from collections.abc import Callable
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
MAPPING_FILE = Path(__file__).parent / "story_migration_map.json"
TESTS_BDD = ROOT / "tests" / "bdd"
CLAUDE_MD = ROOT / "CLAUDE.md"

MILESTONE_TITLES: dict[str, str] = {
    "v0.1.0": "v0.1.0 — Foundation",
    "v0.2.0": "v0.2.0 — Secure Shell",
    "v0.5.0": "v0.5.0 — MVP",
    "v0.8.0": "v0.8.0 — Extended CRM",
    "v1.0.0": "v1.0.0 — Production",
    "v1.1.0": "v1.1.0+ — Post-Production",
}

VERSION_NORMALIZE: dict[str, str] = {
    "v0.1": "v0.1.0",
    "v0.1.0": "v0.1.0",
    "v0.2": "v0.2.0",
    "v0.2.0": "v0.2.0",
    "v0.5": "v0.5.0",
    "v0.5.0": "v0.5.0",
    "v0.8": "v0.8.0",
    "v0.8.0": "v0.8.0",
    "v1.0": "v1.0.0",
    "v1.0.0": "v1.0.0",
    "v1.1": "v1.1.0",
    "v1.1.0": "v1.1.0",
}

CAPABILITY_FALLBACK: dict[str, str] = {
    "authentication": "v0.2.0",
    "shell": "v0.2.0",
    "contacts": "v0.5.0",
    "leads": "v0.5.0",
    "mls": "v0.5.0",
    "telephony": "v0.5.0",
    "calendar": "v0.8.0",
    "tasks": "v0.8.0",
    "properties": "v0.8.0",
    "transactions": "v0.8.0",
    "notifications": "v1.0.0",
    "backup": "v1.0.0",
    "import_export": "v1.0.0",
    "email": "v1.1.0",
    "ai": "v1.1.0",
    "infrastructure": "v0.5.0",
}

CAPABILITY_NORMALIZE: dict[str, str] = {
    "authentication & security": "authentication",
    "authentication": "authentication",
    "app shell": "shell",
    "shell": "shell",
    "contacts": "contacts",
    "leads": "leads",
    "calendar & showings": "calendar",
    "calendar": "calendar",
    "tasks": "tasks",
    "properties": "properties",
    "transactions": "transactions",
    "email": "email",
    "mls integration": "mls",
    "mls": "mls",
    "telephony": "telephony",
    "ai features": "ai",
    "ai": "ai",
    "notifications": "notifications",
    "backup & recovery": "backup",
    "backup": "backup",
    "import & export": "import_export",
    "import_export": "import_export",
    "infrastructure": "infrastructure",
}


def gh(*args: str) -> str:
    result = subprocess.run(
        ["gh", *args], capture_output=True, text=True, encoding="utf-8", check=True
    )
    return result.stdout.strip()


def title_case(text: str) -> str:
    """Capitalise the first letter of each word; leave remaining chars unchanged.

    "macOS build on tag" → "MacOS Build On Tag"
    "HAR MLS listings"   → "HAR MLS Listings"
    """
    return " ".join(word[0].upper() + word[1:] if word else word for word in text.split(" "))


def correct_milestone_key(content: str, capability_key: str) -> str:
    """Return the canonical milestone version key for a story."""
    ms_m = re.search(r"^\*\*Milestone:\*\* (.+)$", content, re.MULTILINE)
    if ms_m:
        full = ms_m.group(1).strip()
        if re.match(r"[Pp]ost-", full) or "TBD" in full.upper():
            return "v1.1.0"
        ver_m = re.search(r"v[\d.]+", full)
        if ver_m:
            return VERSION_NORMALIZE.get(ver_m.group(0), ver_m.group(0))
    return CAPABILITY_FALLBACK.get(capability_key, "")


def build_us_to_issue(mapping: dict[str, int]) -> tuple[dict[int, int], list[int]]:
    """Build {old_US_number → new_issue_number} from the migration filename map.

    Returns (us_map, collision_numbers). Collisions occur when two original
    story files shared the same leading number (e.g. 022-configure-harmls and
    022-windows-installer both map to different issues). The first mapping wins
    in us_map; collision_numbers lists every old number that needs manual review.
    """
    seen: dict[int, list[tuple[str, int]]] = {}
    for filename, issue_num in mapping.items():
        m = re.match(r"^(\d+)-", filename)
        if m:
            old_num = int(m.group(1))
            seen.setdefault(old_num, []).append((filename, issue_num))

    us_map: dict[int, int] = {}
    collisions: list[int] = []
    for old_num, entries in seen.items():
        us_map[old_num] = entries[0][1]  # first mapping wins
        if len(entries) > 1:
            collisions.append(old_num)

    return us_map, collisions


def make_ref_replacer(us_map: dict[int, int]) -> Callable[[re.Match[str]], str]:
    """Replace US-NNN with #N in body text."""

    def _replace(m: re.Match[str]) -> str:
        num = int(m.group(1))
        return f"#{us_map[num]}" if num in us_map else m.group(0)

    return _replace


def make_tag_replacer(us_map: dict[int, int]) -> Callable[[re.Match[str]], str]:
    """Replace @us-NNN / @usNNN with @story_N in BDD tags."""

    def _replace(m: re.Match[str]) -> str:
        num = int(m.group(1))
        return f"@story_{us_map[num]}" if num in us_map else m.group(0)

    return _replace


def update_body_refs(content: str, ref_replacer: Callable[[re.Match[str]], str]) -> str:
    """Replace US-NNN in all sections except Dependencies (already migrated)."""
    lines = content.splitlines(keepends=True)
    in_deps = False
    result: list[str] = []
    for line in lines:
        if re.match(r"^## Dependencies", line):
            in_deps = True
            result.append(line)
        elif in_deps and re.match(r"^## ", line):
            in_deps = False
            result.append(re.sub(r"US-(\d+)", ref_replacer, line))
        elif in_deps:
            result.append(line)
        else:
            result.append(re.sub(r"US-(\d+)", ref_replacer, line))
    return "".join(result)


def apply_bdd_tag_replacements(content: str, tag_replacer: Callable[[re.Match[str]], str]) -> str:
    content = re.sub(r"@us-(\d+)", tag_replacer, content)
    content = re.sub(r"@us(\d+)", tag_replacer, content)
    return content


def main() -> None:
    mapping: dict[str, int] = json.loads(MAPPING_FILE.read_text(encoding="utf-8"))
    us_map, collisions = build_us_to_issue(mapping)

    if collisions:
        print("⚠  US-number collisions — BDD tags for these need manual review:")
        for old_num in sorted(collisions):
            entries = [(f, n) for f, n in mapping.items() if re.match(rf"^0*{old_num}-", f)]
            for fname, inum in entries:
                print(f"   US-{old_num:03d}  {fname}  →  #{inum}")
        print()

    ref_replacer = make_ref_replacer(us_map)
    tag_replacer = make_tag_replacer(us_map)

    # ── Story docs ─────────────────────────────────────────────────────────
    print("Updating story docs...")
    issue_titles: dict[int, str] = {}

    for path in sorted(DOCS.glob("*.md")):
        content = path.read_text(encoding="utf-8")

        issue_m = re.search(r"^\*\*GitHub Issue:\*\* #(\d+)", content, re.MULTILINE)
        if not issue_m:
            print(f"  ⚠  No GitHub Issue field: {path.name}")
            continue
        issue_num = int(issue_m.group(1))

        cap_m = re.search(r"^\*\*Capability:\*\* (.+)$", content, re.MULTILINE)
        cap_raw = cap_m.group(1).strip() if cap_m else "infrastructure"
        capability = CAPABILITY_NORMALIZE.get(cap_raw.lower(), "infrastructure")

        # Determine milestone key before modifying content
        milestone_key = correct_milestone_key(content, capability)
        milestone_title = MILESTONE_TITLES.get(milestone_key, milestone_key)

        # H1: strip old prefix, title-case, reformat as "# N - Title"
        h1_m = re.search(r"^# (.+)$", content, re.MULTILINE)
        if h1_m:
            raw = h1_m.group(1)
            stripped = re.sub(r"^US-\d+ [—\-]+ ?", "", raw).strip()
            stripped = re.sub(r"^\d+ - ", "", stripped).strip()
            new_title_text = title_case(stripped)
            new_h1 = f"# {issue_num} - {new_title_text}"
            content = re.sub(r"^# .+$", new_h1, content, count=1, flags=re.MULTILINE)
            issue_titles[issue_num] = f"{issue_num} - {new_title_text}"

        # Milestone: replace if present, insert after Capability if absent
        if re.search(r"^\*\*Milestone:\*\*", content, re.MULTILINE):
            content = re.sub(
                r"^\*\*Milestone:\*\* .+$",
                f"**Milestone:** {milestone_title}",
                content,
                flags=re.MULTILINE,
            )
        else:
            content = re.sub(
                r"(\*\*Capability:\*\* [^\n]+\n)",
                rf"\1**Milestone:** {milestone_title}\n",
                content,
                count=1,
            )

        # BDD tags in doc body
        content = apply_bdd_tag_replacements(content, tag_replacer)

        # US-NNN body references
        content = update_body_refs(content, ref_replacer)

        path.write_text(content, encoding="utf-8")
        print(f"  ✓ {path.name}")

    # ── GitHub issue titles ────────────────────────────────────────────────
    print(f"\nUpdating {len(issue_titles)} GitHub issue titles...")
    for issue_num in sorted(issue_titles):
        title = issue_titles[issue_num]
        gh("issue", "edit", str(issue_num), "--title", title)
        print(f"  ✓ #{issue_num} → {title}")

    # ── BDD feature files + step defs ─────────────────────────────────────
    bdd_files = sorted(
        list(TESTS_BDD.glob("features/*.feature")) + list(TESTS_BDD.glob("test_*.py"))
    )
    if bdd_files:
        print(f"\nUpdating {len(bdd_files)} BDD file(s)...")
        for path in bdd_files:
            content = path.read_text(encoding="utf-8")
            updated = apply_bdd_tag_replacements(content, tag_replacer)
            if updated != content:
                path.write_text(updated, encoding="utf-8")
                print(f"  ✓ {path.relative_to(ROOT)}")
            else:
                print(f"  ~ {path.relative_to(ROOT)} (unchanged)")
    else:
        print("\nNo BDD files found — nothing to update.")

    # ── CLAUDE.md ──────────────────────────────────────────────────────────
    print("\nUpdating CLAUDE.md...")
    content = CLAUDE_MD.read_text(encoding="utf-8")
    original = content
    content = apply_bdd_tag_replacements(content, tag_replacer)
    # Update pytest command examples: -k "us-NNN" → -m "NNN"
    content = re.sub(
        r'`uv run pytest -k "us-(\d+)"`',
        lambda m: f'`uv run pytest -m "{us_map.get(int(m.group(1)), m.group(1))}"`',
        content,
    )
    if content != original:
        CLAUDE_MD.write_text(content, encoding="utf-8")
        print("  ✓ Updated")
    else:
        print("  ~ Unchanged")

    print("\nDone.")
    if collisions:
        print(
            f"\n⚠  Manually verify BDD tags for US-{collisions[0]:03d} "
            f"(two stories shared this number — see collision report above)."
        )


if __name__ == "__main__":
    main()
