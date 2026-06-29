#!/usr/bin/env python3
"""One-time migration: create GitHub Issues from docs/NNN-*.md story files.

Safe to re-run — already-created issues are skipped using the mapping saved
at scripts/story_migration_map.json after each successful creation.

Usage:
    uv run python scripts/migrate_stories.py
"""

import json
import re
import subprocess
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
MAPPING_FILE = Path(__file__).parent / "story_migration_map.json"

# Milestone version → sort priority (lower = earlier = lower issue numbers)
MILESTONE_ORDER: dict[str, int] = {
    "v0.1.0": 0,
    "v0.2.0": 1,
    "v0.5.0": 2,
    "v0.8.0": 3,
    "v1.0.0": 4,
    "v1.1.0": 5,
}

MILESTONE_TITLES: dict[str, str] = {
    "v0.1.0": "v0.1.0 — Foundation",
    "v0.2.0": "v0.2.0 — Secure Shell",
    "v0.5.0": "v0.5.0 — MVP",
    "v0.8.0": "v0.8.0 — Extended CRM",
    "v1.0.0": "v1.0.0 — Production",
    "v1.1.0": "v1.1.0+ — Post-Production",
}

# Fallback: infer milestone from capability when **Milestone:** is absent
CAPABILITY_MILESTONE_FALLBACK: dict[str, str] = {
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

CAPABILITY_LABELS: dict[str, dict[str, str]] = {
    "authentication": {
        "display": "Authentication & Security",
        "color": "d93f0b",
        "description": "Auth, startup, encryption",
    },
    "shell": {
        "display": "App Shell",
        "color": "0075ca",
        "description": "Main window, navigation, settings",
    },
    "contacts": {
        "display": "Contacts",
        "color": "e4e669",
        "description": "Contact CRUD, search, tags",
    },
    "leads": {
        "display": "Leads",
        "color": "a2eeef",
        "description": "Lead management, pipeline",
    },
    "calendar": {
        "display": "Calendar & Showings",
        "color": "7057ff",
        "description": "Calendar events, showings",
    },
    "tasks": {
        "display": "Tasks",
        "color": "008672",
        "description": "Task management",
    },
    "properties": {
        "display": "Properties",
        "color": "e11d48",
        "description": "Property listings",
    },
    "transactions": {
        "display": "Transactions",
        "color": "fb8500",
        "description": "Transaction tracking",
    },
    "email": {
        "display": "Email",
        "color": "6f42c1",
        "description": "Email integration",
    },
    "mls": {
        "display": "MLS Integration",
        "color": "0e8a16",
        "description": "HAR MLS integration",
    },
    "telephony": {
        "display": "Telephony",
        "color": "b60205",
        "description": "Google Voice, Twilio calling",
    },
    "ai": {
        "display": "AI Features",
        "color": "1d76db",
        "description": "AI features",
    },
    "notifications": {
        "display": "Notifications",
        "color": "f9d0c4",
        "description": "Desktop and in-app notifications",
    },
    "backup": {
        "display": "Backup & Recovery",
        "color": "c2e0c6",
        "description": "Backup and recovery",
    },
    "import_export": {
        "display": "Import & Export",
        "color": "fef2c0",
        "description": "Import and export",
    },
    "infrastructure": {
        "display": "Infrastructure",
        "color": "bfd4f2",
        "description": "CI/CD, build, dev setup",
    },
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


@dataclass
class Story:
    path: Path
    number: int
    slug: str
    title: str
    capability_key: str
    milestone: str
    status: str
    content: str
    issue_number: int = field(default=0)


def normalize_capability(raw: str) -> str:
    return CAPABILITY_NORMALIZE.get(raw.strip().lower(), "infrastructure")


def parse_story(path: Path) -> Story | None:
    m = re.match(r"^(\d+)-(.+)\.md$", path.name)
    if not m:
        return None
    number = int(m.group(1))
    slug = m.group(2)
    content = path.read_text(encoding="utf-8")

    title_m = re.search(r"^# (.+)$", content, re.MULTILINE)
    title = title_m.group(1) if title_m else path.stem

    cap_m = re.search(r"^\*\*Capability:\*\* (.+)$", content, re.MULTILINE)
    capability_key = normalize_capability(cap_m.group(1) if cap_m else "infrastructure")

    ms_m = re.search(r"^\*\*Milestone:\*\* (v[\d.]+)", content, re.MULTILINE)
    milestone = ms_m.group(1) if ms_m else CAPABILITY_MILESTONE_FALLBACK.get(capability_key, "")

    status_m = re.search(r"^\*\*Status:\*\* (.+)$", content, re.MULTILINE)
    status = status_m.group(1).strip() if status_m else "Not Started"

    return Story(
        path=path,
        number=number,
        slug=slug,
        title=title,
        capability_key=capability_key,
        milestone=milestone,
        status=status,
        content=content,
    )


def sort_key(story: Story) -> tuple[int, int]:
    return (MILESTONE_ORDER.get(story.milestone, 99), story.number)


def gh(*args: str) -> str:
    result = subprocess.run(
        ["gh", *args], capture_output=True, text=True, encoding="utf-8", check=True
    )
    return result.stdout.strip()


def setup_labels() -> None:
    print("Setting up labels...")
    for meta in CAPABILITY_LABELS.values():
        gh(
            "label",
            "create",
            meta["display"],
            "--color",
            meta["color"],
            "--description",
            meta["description"],
            "--force",
        )
        print(f"  ✓ {meta['display']}")


def setup_milestones() -> None:
    print("Setting up milestones...")
    # --jq outputs one title per line; handles pagination automatically
    existing_raw = gh(
        "api",
        "repos/:owner/:repo/milestones",
        "--paginate",
        "--jq",
        ".[].title",
    )
    existing_titles = set(existing_raw.splitlines())
    for title in MILESTONE_TITLES.values():
        if title in existing_titles:
            print(f"  ~ {title} (already exists)")
            continue
        gh(
            "api",
            "repos/:owner/:repo/milestones",
            "--method",
            "POST",
            "--field",
            f"title={title}",
        )
        print(f"  ✓ {title}")


def create_issue(story: Story) -> int:
    label = CAPABILITY_LABELS[story.capability_key]["display"]
    args = [
        "issue",
        "create",
        "--title",
        story.title,
        "--body",
        story.content,
        "--label",
        label,
    ]
    if story.milestone in MILESTONE_TITLES:
        args += ["--milestone", MILESTONE_TITLES[story.milestone]]
    url = gh(*args)
    return int(url.rstrip("/").split("/")[-1])


def _make_us_replacer(us_to_issue: dict[int, int]) -> Callable[[re.Match[str]], str]:
    def _replace(m: re.Match[str]) -> str:
        num = int(m.group(1))
        return f"#{us_to_issue[num]}" if num in us_to_issue else m.group(0)

    return _replace


def update_file(path: Path, issue_number: int, us_to_issue: dict[int, int]) -> None:
    content = path.read_text(encoding="utf-8")

    # Insert **GitHub Issue:** after **Status:** if not already present
    if "**GitHub Issue:**" not in content:
        content = re.sub(
            r"(\*\*Status:\*\* [^\n]+\n)",
            rf"\1**GitHub Issue:** #{issue_number}\n",
            content,
        )

    # Replace US-NNN references inside the Dependencies section only
    replacer = _make_us_replacer(us_to_issue)
    lines = content.splitlines(keepends=True)
    in_deps = False
    updated: list[str] = []
    for line in lines:
        if re.match(r"^## Dependencies", line):
            in_deps = True
            updated.append(line)
        elif in_deps and re.match(r"^## ", line):
            in_deps = False
            updated.append(line)
        elif in_deps:
            updated.append(re.sub(r"US-(\d+)", replacer, line))
        else:
            updated.append(line)

    path.write_text("".join(updated), encoding="utf-8")


def main() -> None:
    mapping: dict[str, int] = {}
    if MAPPING_FILE.exists():
        mapping = json.loads(MAPPING_FILE.read_text())

    stories: list[Story] = []
    for path in DOCS.glob("*.md"):
        story = parse_story(path)
        if story:
            stories.append(story)
    stories.sort(key=sort_key)
    print(f"Found {len(stories)} stories\n")

    setup_labels()
    print()
    setup_milestones()
    print()

    print("Creating issues...")
    for story in stories:
        if story.path.name in mapping:
            story.issue_number = mapping[story.path.name]
            print(f"  ~ #{story.issue_number} {story.title} (already created)")
            continue
        issue_number = create_issue(story)
        story.issue_number = issue_number
        if story.status == "Done":
            gh("issue", "close", str(issue_number))
        mapping[story.path.name] = issue_number
        MAPPING_FILE.write_text(json.dumps(mapping, indent=2))
        print(f"  ✓ #{issue_number} {story.title}")

    us_to_issue: dict[int, int] = {s.number: s.issue_number for s in stories}

    print("\nUpdating and renaming files...")
    for story in stories:
        update_file(story.path, story.issue_number, us_to_issue)
        new_path = DOCS / f"{story.issue_number}-{story.slug}.md"
        if story.path.name != new_path.name:
            story.path.rename(new_path)
            print(f"  ✓ {story.path.name} → {new_path.name}")

    print(f"\nDone. Mapping saved to {MAPPING_FILE}")


if __name__ == "__main__":
    main()
