# Linux Build — Manual Tests

**Story:** [US-193 — Linux Build on Tag](../../../docs/193-linux-build.md)

## Linux executable is attached to the release

1. Push a `feat:` commit to main and wait for the release workflow to complete
2. Navigate to the GitHub Release page
3. Verify the Linux executable is listed as a release asset alongside the Windows and macOS artifacts

## Linux executable runs correctly

1. Download the Linux executable from the GitHub Release
2. Run it on a Linux machine
3. Verify the window appears with "OurCRM" in the title
4. Verify the app shuts down cleanly when closed

## Linux build failure blocks the release

1. Introduce a build error specific to the ubuntu-latest matrix job and push a `feat:` commit
2. Verify the Linux build job fails
3. Verify no GitHub Release is published
4. Revert the error
