# US-005: Build Standalone Executable

## User Story

**As a** developer  
**I want to** build a standalone executable  
**So that** I can test the distribution process and verify the app works without Python installed

## Priority

**MVP:** Must Have

**Rationale:** The app is meant to be distributed as standalone executables for non-technical users. Building and testing this process early validates the distribution strategy.

## Estimated Effort

**Size:** Medium (M) - 3-5 days

**Breakdown:**
- 2 hours: Install and configure Nuitka
- 3 hours: Create build script
- 4 hours: Configure platform-specific builds (Windows, macOS, Linux)
- 4 hours: Test builds on each platform
- 3 hours: Document build process
- 2 hours: Optimize build configuration

## Dependencies

**Depends on:** US-001 (Setup Development Environment), US-002 (Run Application)

**Blocks:** US-190, US-191, US-192 (Download Executables for each platform)

## Description

A developer should be able to build a standalone executable for Windows, macOS, or Linux with a simple command. The executable should run on systems without Python installed and include all necessary dependencies. The build process should be reproducible and documented.

The build process must handle platform-specific requirements (like code signing on macOS, if needed later) and produce a single file or app bundle that users can download and run. The resulting executable should be tested to ensure it works the same as the development version.

## Acceptance Criteria

- [ ] Build command works on Windows — see tests/manual/infrastructure.md
- [ ] Build command works on macOS — see tests/manual/infrastructure.md
- [ ] Build command works on Linux — see tests/manual/infrastructure.md
- [ ] Built executable runs without Python installed — see tests/manual/infrastructure.md
- [ ] Built executable includes all dependencies — see tests/manual/infrastructure.md
- [x] Build process is documented in README
- [ ] Build process is reproducible — see tests/manual/infrastructure.md
- [ ] Build completes in reasonable time (under 30 minutes) — see tests/manual/infrastructure.md
- [ ] Resulting executable launches successfully — see tests/manual/infrastructure.md
- [ ] All features work in the built executable — see tests/manual/infrastructure.md
- [ ] Build script handles platform-specific requirements — see tests/manual/infrastructure.md
- [ ] Build output is predictable and consistent — see tests/manual/infrastructure.md