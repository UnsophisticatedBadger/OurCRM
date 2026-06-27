# US-002 — Build Executable on Tag

**Capability:** infrastructure
**Status:** Not Done

## User Story

As a developer, I want standalone executables built and published automatically when I push a version tag, so that every release is reproducible, traceable to a specific commit, and ready to download without a manual build step.

## Dependencies

- US-001 — CI Pipeline

## Acceptance Criteria

1. Pushing a `v*.*.*` tag triggers the release workflow; no other push triggers it
2. Windows, macOS, and Linux executables are built in parallel using matrix builds with `scripts/build.py` as the driver
3. A GitHub Release is created automatically using the tag name; release notes include the tag and commit SHA
4. Build failures prevent the release from being published
5. Windows `.exe`, macOS `.app` bundle, and Linux executable are attached to the release as downloadable assets

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/infrastructure.feature` |
| BDD step defs | `tests/bdd/test_infrastructure.py` |
| Unit tests | `tests/unit/infrastructure/test_build_script.py` |
| Manual tests | `tests/manual/infrastructure/release_workflow.md` |

## Definition of Done

- [x] BDD scenarios pass
- [x] `ruff`, `mypy --strict` clean
- [ ] Release artifacts verified manually by pushing a real `v*.*.*` tag and confirming all three platform executables are attached to the GitHub Release
