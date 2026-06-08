# US-002: Run the Application

## User Story

**As a** developer  
**I want to** run the application from the command line  
**So that** I can test changes and see the app in action

## Priority

**MVP:** Must Have

**Rationale:** Without a runnable application, no development can be tested or demonstrated. This builds directly on US-001.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Create entry point script
- 1 hour: Wire up PySide6 application
- 1 hour: Create basic main window
- 2 hours: Test on all platforms
- 1 hour: Document command usage

## Dependencies

**Depends on:** US-001 (Setup Development Environment)

**Blocks:** US-003 (Run Linters), US-004 (Run Test Suite), US-005 (Build Executable)

## Description

After completing setup, a developer should be able to launch OurCRM by running a single command. The application should open a window with the OurCRM title and display a basic interface. The command should work consistently across Windows, macOS, and Linux.

The app should be runnable via `uv run ourcrm` from the project root directory. It should open quickly (within 5 seconds on standard hardware) and display a window that can be closed normally.

## BDD Scenarios

### Scenario 1: Launch app from project directory

```
Given I am in the OurCRM project root directory
  And all dependencies are installed
When I run "uv run ourcrm"
Then the application should launch
  And a window should appear on screen
  And the window title should be "OurCRM"
```

### Scenario 2: Launch app from subdirectory

```
Given I am in a subdirectory of the OurCRM project
  And all dependencies are installed
When I run "uv run ourcrm"
Then the application should launch successfully
```

### Scenario 3: Close the application normally

```
Given the application is running
When I close the window using the standard close button
Then the application should exit cleanly
  And no error messages should appear
  And the process should terminate
```

### Scenario 4: Launch app on Windows

```
Given I am on Windows
  And I have completed setup
When I run "uv run ourcrm"
Then the application should launch
  And the window should appear
  And the console should not show Python errors
```

### Scenario 5: Launch app on macOS

```
Given I am on macOS
  And I have completed setup
When I run "uv run ourcrm"
Then the application should launch
  And the window should appear in the dock
  And the menu bar should show the application name
```

### Scenario 6: Launch app on Linux

```
Given I am on Linux
  And I have completed setup
When I run "uv run ourcrm"
Then the application should launch
  And the window should appear
  And it should work with common desktop environments (GNOME, KDE, XFCE)
```

## Manual Testing Steps

### Test 1: Verify app launches on each platform

1. Run `uv run ourcrm` on Windows
2. Verify window appears
3. Close the window
4. Verify no error dialogs appear
5. Repeat for macOS
6. Repeat for Linux
7. Document any platform-specific issues

### Test 2: Verify window properties

1. Launch the application
2. Check that the window has a title bar showing "OurCRM"
3. Check that the window can be resized
4. Check that the window can be moved
5. Check that the window can be minimized and maximized
6. Check that the window has proper close/minimize/maximize buttons for the OS

### Test 3: Verify clean shutdown

1. Launch the application
2. Close it using the window close button
3. Check that no Python traceback or error messages appear
4. Check that the process exits (no zombie processes)
5. Check that system resources are released (memory, file handles)

### Test 4: Verify startup time

1. Close the application if running
2. Note the current time
3. Run `uv run ourcrm`
4. Measure how long until the window appears
5. Verify it's under 5 seconds on standard hardware
6. Repeat 3 times to get consistent measurement

### Test 5: Verify error handling for missing dependencies

1. Temporarily rename or hide a required dependency
2. Try to run the application
3. Verify a clear error message appears
4. Verify the error message tells the user what's missing
5. Restore the dependency

## Acceptance Criteria

- [ ] `uv run ourcrm` launches the application
- [ ] Window appears with "OurCRM" in the title
- [ ] Application launches on Windows, macOS, and Linux
- [ ] Startup time is under 5 seconds
- [ ] Application closes cleanly without errors
- [ ] No Python traceback or error messages on normal use
- [ ] Window can be resized, moved, minimized, and maximized
- [ ] All UI elements render correctly on all platforms
- [ ] Process exits cleanly (no zombie processes)
- [ ] Error messages are clear if dependencies are missing