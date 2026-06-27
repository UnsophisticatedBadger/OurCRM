# Release Workflow — Manual Tests

**Story:** [US-002 — Build Executable on Tag](../../../docs/002-build-executable-on-tag.md)

## Pushing a version tag triggers the release workflow

1. Push a version tag: `git tag v0.1.0 && git push origin v0.1.0`
2. Open GitHub Actions
3. Verify the release workflow starts
4. Verify matrix jobs run for windows-latest, macos-latest, and ubuntu-latest

## Non-version tags do not trigger the release workflow

1. Push a tag that does not match `v*.*.*`: `git tag beta-1 && git push origin beta-1`
2. Open GitHub Actions
3. Verify the release workflow does NOT appear in the run list

## GitHub Release is created with all three platform assets

1. Wait for all matrix jobs to complete successfully
2. Navigate to the Releases page on GitHub
3. Verify a release named `v0.1.0` exists
4. Verify Windows `.exe`, macOS `.app` bundle, and Linux executable are attached as assets
5. Verify release notes include the tag name and commit SHA

## Build failure prevents the release from being published

1. Introduce a build error and push a new version tag
2. Verify the failing matrix job blocks the release creation step
3. Verify no GitHub Release is created for that tag
4. Revert the error

## Executables run on their native platforms

1. Download the Windows executable from the release and run it on Windows
2. Download the macOS bundle and run it on macOS
3. Download the Linux executable and run it on Linux
4. On each platform: verify the window appears with "OurCRM" in the title and shuts down cleanly
