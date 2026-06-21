# US-174: Build Executable on Tag

## User Story

**As a** developer
**I want to** automatically build and publish standalone executables when I push a version tag
**So that** releases are reproducible and attached to a specific git commit

## Priority

**MVP:** Must Have

**Rationale:** Manual builds are error-prone and hard to reproduce. Tying builds to git tags ensures every release is traceable and consistent.

## Estimated Effort

**Size:** Medium (M) - 2-3 days

**Breakdown:**
- 2 hours: Create GitHub Actions release workflow
- 2 hours: Configure Nuitka build step for Windows
- 2 hours: Configure Nuitka build step for macOS
- 2 hours: Configure Nuitka build step for Linux
- 2 hours: Wire up GitHub Release creation and artifact upload
- 2 hours: Test end-to-end with a test tag

## Dependencies

**Depends on:** US-005 (Build Standalone Executable), US-173 (CI Pipeline)

**Blocks:** US-190, US-191, US-192 (Download Executables for each platform)

## Description

A GitHub Actions workflow triggers when a tag matching `v*.*.*` is pushed. It builds standalone executables for Windows, macOS, and Linux in parallel using matrix builds, then creates a GitHub Release and attaches the executables as downloadable assets.

The workflow uses `scripts/build.py` (from US-005) as the build driver. Each platform runner produces its native executable in `dist/`.

## Acceptance Criteria

- [x] Workflow file exists at `.github/workflows/release.yml`
- [x] Workflow triggers only on `v*.*.*` tags
- [x] Matrix builds run for windows-latest, macos-latest, ubuntu-latest
- [x] Each build uses `scripts/build.py` as the build driver
- [x] GitHub Release is created automatically with the tag name
- [ ] Windows .exe is attached to the release — see tests/manual/ci-cd.md
- [ ] macOS .app bundle is attached to the release — see tests/manual/ci-cd.md
- [ ] Linux executable is attached to the release — see tests/manual/ci-cd.md
- [x] Build failures prevent the release from being published
- [x] Release notes include the tag and commit SHA
