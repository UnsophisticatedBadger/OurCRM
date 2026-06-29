# US-022 — Windows Installer

**Capability:** infrastructure
**Milestone:** v0.5.0 — MVP
**Status:** Not Started
**GitHub Issue:** #50

## User Story

As a developer, I want a proper Windows installer published with each release so that the primary user can install OurCRM on Windows with a standard installer that creates a Start Menu shortcut, handles upgrades cleanly, and provides an uninstaller.

## Dependencies

- #2 — Automated Release Pipeline

## Acceptance Criteria

1. An Inno Setup script (`scripts/installer.iss`) packages the Nuitka standalone output into a single `.exe` installer
2. The installer places OurCRM in `%LocalAppData%\OurCRM` (no admin rights required)
3. The installer creates a Start Menu shortcut named "OurCRM"
4. The installer registers an uninstaller accessible from Windows Settings → Apps
5. Running the installer again over an existing installation upgrades it cleanly without requiring a manual uninstall first
6. The release workflow runs Inno Setup on `windows-latest` after the Nuitka build and attaches `ourcrm-setup.exe` to the GitHub Release
7. The interim `ourcrm-windows.zip` asset is removed from the release; the installer replaces it as the sole Windows download
8. A build or packaging failure prevents the release from being published

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/infrastructure.feature` |
| BDD step defs | `tests/bdd/test_infrastructure.py` |
| Manual tests | `tests/manual/infrastructure/windows_installer.md` |

## Definition of Done

- [ ] BDD scenarios pass
- [ ] `ruff`, `mypy --strict` clean
- [ ] Installer verified by the primary user: installs cleanly, shortcut works, app opens, uninstaller removes it without leftovers
