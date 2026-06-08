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

## BDD Scenarios

### Scenario 1: Build Windows executable

```
Given I am on Windows
  And I am in the project root directory
When I run the Windows build command
Then the build should complete successfully
  And an executable file should be created in the dist/ directory
  And the executable should have a .exe extension
```

### Scenario 2: Build macOS application

```
Given I am on macOS
  And I am in the project root directory
When I run the macOS build command
Then the build should complete successfully
  And an application bundle should be created in the dist/ directory
  And the bundle should have a .app extension
```

### Scenario 3: Build Linux executable

```
Given I am on Linux
  And I am in the project root directory
When I run the Linux build command
Then the build should complete successfully
  And an executable file should be created in the dist/ directory
```

### Scenario 4: Verify executable runs without Python

```
Given I have built an executable
  And the system does not have Python installed (or it's not in PATH)
When I run the executable
Then the application should launch
  And the window should appear
  And the app should function normally
```

### Scenario 5: Verify executable includes dependencies

```
Given I have built an executable
When I examine the executable
Then it should be a single file or self-contained bundle
  And it should not require separate installation of dependencies
```

## Manual Testing Steps

### Test 1: Verify build process completes

1. Navigate to the project root directory
2. Run the build command for your platform
3. Wait for the build to complete
4. Verify the executable was created
5. Check the file size is reasonable (not suspiciously small or huge)
6. Check the build log for any warnings

### Test 2: Verify executable launches

1. Navigate to the dist/ directory
2. Double-click the executable (or run from command line)
3. Verify the application window appears
4. Verify the window has the correct title
5. Test basic functionality (window can be moved, resized, closed)
6. Close the application

### Test 3: Verify executable works on clean system

1. Test the executable on a system without Python installed
2. Or test on a system where Python is not in PATH
3. Verify the application still launches
4. Verify all features work
5. Document the system configuration used for testing

### Test 4: Verify cross-platform builds

1. Build on Windows, verify .exe is created
2. Build on macOS, verify .app is created
3. Build on Linux, verify executable is created
4. Test each executable on its target platform
5. Document any platform-specific issues

### Test 5: Verify build is reproducible

1. Clean the build directory
2. Run the build command again
3. Verify the build succeeds
4. Verify the resulting executable works the same way
5. Check that the build process is consistent

### Test 6: Verify executable handles missing files gracefully

1. Build the executable
2. Move it to a different directory
3. Try to run it
4. Verify it either works (if dependencies are bundled) or shows a clear error message
5. Document the behavior

### Test 7: Check executable size and performance

1. Build the executable
2. Note the file size
3. Launch the executable
4. Measure startup time
5. Verify the startup time is reasonable (under 10 seconds)
6. Compare with the development version's startup time

## Acceptance Criteria

- [ ] Build command works on Windows
- [ ] Build command works on macOS
- [ ] Build command works on Linux
- [ ] Built executable runs without Python installed
- [ ] Built executable includes all dependencies
- [ ] Build process is documented in README
- [ ] Build process is reproducible
- [ ] Build completes in reasonable time (under 30 minutes)
- [ ] Resulting executable launches successfully
- [ ] All features work in the built executable
- [ ] Build script handles platform-specific requirements
- [ ] Build output is predictable and consistent