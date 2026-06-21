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

## Acceptance Criteria

- [x] `uv run ourcrm` launches the application
- [x] Window appears with "OurCRM" in the title
- [ ] Application launches on Windows, macOS, and Linux — see tests/manual/infrastructure.md
- [ ] Startup time is under 5 seconds — see tests/manual/infrastructure.md
- [x] Application closes cleanly without errors
- [x] No Python traceback or error messages on normal use
- [x] Window can be resized, moved, minimized, and maximized
- [ ] All UI elements render correctly on all platforms — see tests/manual/infrastructure.md
- [x] Process exits cleanly (no zombie processes)
- [ ] Error messages are clear if dependencies are missing — see tests/manual/infrastructure.md