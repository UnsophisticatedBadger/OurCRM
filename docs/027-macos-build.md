# US-027 — macOS Build on Tag

**Capability:** infrastructure
**Milestone:** v0.5.0 — MVP
**Status:** Not Started

## User Story

As a developer, I want a macOS executable built and published automatically alongside the Windows build when I push a version tag, so that the primary user can download and run OurCRM on macOS from the first MVP release.

## Dependencies

- US-002 — Automated Release Pipeline

## Acceptance Criteria

1. The release workflow matrix is extended to include `macos-latest`
2. The macOS `.app` bundle is built using `scripts/build.py` as the driver
3. The macOS bundle is attached to the GitHub Release alongside the Windows executable
4. A macOS build failure prevents the release from being published

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/infrastructure.feature` |
| BDD step defs | `tests/bdd/test_infrastructure.py` |
| Unit tests | `tests/unit/infrastructure/test_build_script.py` |
| Manual tests | `tests/manual/infrastructure/macos_build.md` |

## Definition of Done

- [ ] BDD scenarios pass
- [ ] `ruff`, `mypy --strict` clean
- [ ] macOS `.app` bundle verified by the primary user: app opens, window shows "OurCRM", shuts down cleanly
