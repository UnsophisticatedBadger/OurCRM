"""Shared milestone mapping for story-doc and GitHub-milestone tooling.

Milestone titles are capability names only (no version prefix) — GitHub
issue/PR version numbers are assigned automatically by semantic-release per
commit, so they can't be pre-mapped to a milestone plan. See docs/4's story
thread for context if this needs re-litigating.
"""

import re

# Internal keys stay version-shaped only because they mirror the historical
# v0.1.0/v0.2.0/... milestone ordering — they are not displayed anywhere.
MILESTONE_TITLES: dict[str, str] = {
    "v0.1.0": "Foundation",
    "v0.2.0": "Secure Shell",
    "v0.5.0": "MVP",
    "v0.8.0": "Extended CRM",
    "v1.0.0": "Production",
    "v1.1.0": "Post-Production",
}

MILESTONE_ORDER: dict[str, int] = {
    "v0.1.0": 0,
    "v0.2.0": 1,
    "v0.5.0": 2,
    "v0.8.0": 3,
    "v1.0.0": 4,
    "v1.1.0": 5,
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


def correct_milestone_key(content: str, capability_key: str) -> str:
    """Return the canonical milestone key (e.g. "v0.2.0") for a story doc.

    Matches the current version-less **Milestone:** field (e.g. "Secure Shell")
    against known titles first; falls back to parsing a legacy version-prefixed
    field (e.g. "v0.2.0 — Secure Shell") for any doc not yet migrated; falls
    back to the capability's default milestone if the field is absent.
    """
    ms_m = re.search(r"^\*\*Milestone:\*\* (.+)$", content, re.MULTILINE)
    if ms_m:
        full = ms_m.group(1).strip()
        for key, title in MILESTONE_TITLES.items():
            if full == title:
                return key
        if re.match(r"[Pp]ost-", full) or "TBD" in full.upper():
            return "v1.1.0"
        ver_m = re.search(r"v[\d.]+", full)
        if ver_m:
            return VERSION_NORMALIZE.get(ver_m.group(0), ver_m.group(0))
    return CAPABILITY_FALLBACK.get(capability_key, "")
