# US-002 — Automated Release Pipeline

**Capability:** infrastructure
**Status:** Not Done

## User Story

As a developer, I want version numbers managed automatically and a Windows executable published on every release, so that tagging is driven by commit history and every release is reproducible and ready to download without manual steps.

## Dependencies

- US-001 — CI Pipeline

## Acceptance Criteria

1. `feat:` commits on main trigger a minor version bump; `fix:`/`perf:`/`refactor:` commits trigger a patch bump; a `BREAKING CHANGE` footer triggers a major bump
2. On every push to main, `python-semantic-release` determines whether a new version is warranted; if so, it updates `pyproject.toml`, commits the bump, creates a `v*.*.*` tag, and pushes both
3. A new version tag triggers a Windows build using `scripts/build.py` as the driver
4. A GitHub Release is created automatically using the tag name with the tag in the release notes
5. The Windows executable is attached to the release as a downloadable asset
6. If no commits warrant a version bump, no tag is created and no build runs
7. A build failure prevents the release from being published
8. A `README.md` exists at the project root covering: what OurCRM is, who it is for, dev environment setup, how to run tests and linters, and a link to the wiki roadmap

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/infrastructure.feature` |
| BDD step defs | `tests/bdd/test_infrastructure.py` |
| Unit tests | `tests/unit/infrastructure/test_build_script.py` |
| Unit tests | `tests/unit/infrastructure/test_release_config.py` |
| Manual tests | `tests/manual/infrastructure/release_workflow.md` |

## Definition of Done

- [ ] BDD scenarios pass
- [ ] `ruff`, `mypy --strict` clean
- [ ] Push a `feat:` commit to main; confirm semantic-release creates `v0.1.0`, the build job runs, and the Windows executable is attached to the GitHub Release
