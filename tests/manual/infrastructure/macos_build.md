# macOS Build — Manual Tests

**Story:** [US-003 — macOS Build on Tag](../../../docs/003-macos-build.md)

## macOS app bundle is attached to the release

1. Push a `feat:` commit to main and wait for the release workflow to complete
2. Navigate to the GitHub Release page
3. Verify the macOS `.app` bundle is listed as a release asset alongside the Windows executable

## macOS app bundle runs correctly

1. Download the macOS `.app` bundle from the GitHub Release
2. Open it on a macOS machine
3. Verify the window appears with "OurCRM" in the title
4. Verify the app shuts down cleanly when closed

## macOS build failure blocks the release

1. Introduce a build error specific to the macOS matrix job and push a `feat:` commit
2. Verify the macOS build job fails
3. Verify no GitHub Release is published
4. Revert the error
