# 103 - Linux Build On Tag

**Capability:** infrastructure
**Milestone:** Post-Production
**Status:** Not Started
**GitHub Issue:** #103
**Priority:** Low — Linux is not required by the primary user or either development platform

## User Story

As a developer, I want a Linux executable built and published automatically alongside the Windows and macOS builds when I push a version tag, so that all three platform artifacts are available in every release.

## Dependencies

- #3 — macOS Build on Tag

## Acceptance Criteria

1. The release workflow matrix is extended to include `ubuntu-latest`
2. The Linux executable is built using `scripts/build.py` as the driver
3. The Linux executable is attached to the GitHub Release alongside the Windows and macOS artifacts
4. A Linux build failure prevents the release from being published

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/infrastructure.feature` |
| BDD step defs | `tests/bdd/test_infrastructure.py` |
| Unit tests | `tests/unit/infrastructure/test_build_script.py` |
| Manual tests | `tests/manual/infrastructure/linux_build.md` |

## Definition of Done

- [ ] BDD scenarios pass
- [ ] `ruff`, `mypy --strict` clean
- [ ] Linux executable verified by running the built artifact on a Linux machine
- [ ] Wiki documentation written, or marked N/A with a reason
