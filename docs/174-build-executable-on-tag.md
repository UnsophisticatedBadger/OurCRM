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

## BDD Scenarios

### Scenario 1: Workflow triggers on version tag

```
Given a tag matching "v*.*.*" is pushed
When the release workflow runs
Then builds start for Windows, macOS, and Linux
  And a GitHub Release is created with the tag name
```

### Scenario 2: Windows executable is attached to release

```
Given the Windows build job completes
When the release is published
Then a .exe file is attached as a release asset
  And the asset is downloadable
```

### Scenario 3: Workflow does not trigger on non-version tags

```
Given a tag not matching "v*.*.*" is pushed
When GitHub evaluates the workflow trigger
Then the release workflow does not run
```

## Manual Testing Steps

### Test 1: Verify tag trigger

1. Push a tag: `git tag v0.1.0 && git push origin v0.1.0`
2. Open GitHub Actions
3. Verify the release workflow starts
4. Verify matrix jobs run for each platform

### Test 2: Verify GitHub Release is created

1. Wait for all matrix jobs to complete
2. Navigate to the Releases page
3. Verify a release named `v0.1.0` exists
4. Verify all three platform executables are attached

### Test 3: Verify executables work

1. Download each platform executable from the release
2. Run each on its native platform
3. Verify the window appears with "OurCRM" in the title
4. Verify clean shutdown

## Acceptance Criteria

- [ ] Workflow file exists at `.github/workflows/release.yml`
- [ ] Workflow triggers only on `v*.*.*` tags
- [ ] Matrix builds run for windows-latest, macos-latest, ubuntu-latest
- [ ] Each build uses `scripts/build.py` as the build driver
- [ ] GitHub Release is created automatically with the tag name
- [ ] Windows .exe is attached to the release
- [ ] macOS .app bundle is attached to the release
- [ ] Linux executable is attached to the release
- [ ] Build failures prevent the release from being published
- [ ] Release notes include the tag and commit SHA
