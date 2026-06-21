# US-015: Create the First Window

## User Story

**As a** user  
**I want to** see the main application window after logging in  
**So that** I can start using OurCRM

## Priority

**MVP:** Must Have

**Rationale:** After successful authentication, users need to see the main application interface. This is the foundation for all user interactions with the application.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 2 hours: Design main window layout
- 3 hours: Create main window UI with PySide6
- 2 hours: Add menu bar and toolbar
- 2 hours: Implement navigation between sections
- 1 hour: Add status bar
- 2 hours: Implement window state persistence
- 2 hours: Test cross-platform window behavior
- 2 hours: Test window resizing and responsiveness

## Dependencies

**Depends on:** US-002 (Run Application), US-011 (Log In)

**Blocks:** US-016 (Navigate Between Sections), all UI features

## Description

After successful login, the user should see the main application window. This window serves as the primary interface for OurCRM and provides access to all major features. The window should have a menu bar, toolbar, navigation panel, and main content area.

The window should be responsive, resizable, and remember its size and position between sessions. It should follow the platform's native window conventions (close, minimize, maximize buttons in the correct location, proper menu bar behavior on macOS, etc.).

## Acceptance Criteria

- [x] Main window appears after successful login
- [x] Window has menu bar, toolbar, navigation, and content area
- [x] Window is resizable
- [x] Window remembers size and position between sessions
- [ ] Window follows platform-specific conventions — see tests/manual/app-shell.md
- [x] All menu items are functional
- [x] Window controls work correctly (minimize, maximize, close)
- [x] Application closes cleanly
- [ ] Works on Windows, macOS, and Linux — see tests/manual/app-shell.md
- [x] Window is responsive and layout adjusts to size
- [x] Status bar shows relevant information
- [x] Navigation panel is clear and intuitive