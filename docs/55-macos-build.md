# 55 - MacOS Build On Tag

**Capability:** infrastructure
**Milestone:** MVP
**Status:** Not Started
**GitHub Issue:** #55

## User Story

As a developer, I want a macOS executable built and published automatically alongside the Windows build when I push a version tag, so that the primary user can download and run OurCRM on macOS from the first MVP release.

## Dependencies

- #2 — Automated Release Pipeline

## Acceptance Criteria

1. The release workflow matrix is extended to include `macos-latest`
2. The macOS `.app` bundle is built using `scripts/build.py` as the driver
3. After the build, `scripts/build.py` wraps the `.app` bundle in a `.dmg` disk image using `hdiutil` (built into macOS — no extra tooling required)
4. The `.dmg` contains `OurCRM.app` and a symlink to `/Applications` so the user sees the standard drag-to-install layout
5. The disk image is named `ourcrm-macos.dmg` and attached to the GitHub Release alongside the Windows zip
6. A macOS build or packaging failure prevents the release from being published

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
- [ ] DMG verified by the primary user: mounts cleanly, drag-to-Applications works, app opens from Applications folder, no quarantine warnings block launch
- [ ] Wiki documentation written, or marked N/A with a reason
