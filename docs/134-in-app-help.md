# US-134: In-App Help & Documentation

## User Story

**As a** user  
**I want to** access help and documentation from within the app  
**So that** I can learn how to use features and get help when I need it

## Priority

**MVP:** Should Have

**Rationale:** Users need help learning the system and troubleshooting issues. In-app help reduces support requests and improves user satisfaction. This includes a user guide, keyboard shortcuts reference, and about dialog.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design help menu structure
- 2 hours: Create help window with documentation
- 1 hour: Add keyboard shortcuts reference
- 1 hour: Create About dialog
- 1 hour: Add tooltips (basic)
- 1 hour: Test help functionality
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-015 (Create the First Window)

**Blocks:** None

## Description

Users should be able to access help from the Help menu. The help system should include:
1. **User Guide**: Basic documentation on how to use major features
2. **Keyboard Shortcuts**: Reference of all keyboard shortcuts
3. **About Dialog**: Version info, copyright, links to website/support
4. **Tooltips**: Basic hover tooltips on key UI elements

For MVP, the documentation can be embedded or link to online docs.

## Acceptance Criteria

- [x] Help menu is available
- [x] User Guide is accessible
- [x] Keyboard Shortcuts reference is available
- [x] About dialog shows version and info
- [x] Tooltips appear on hover for key elements
- [ ] Help content is searchable — not yet implemented
- [x] Help works offline (embedded or cached)
- [x] Help opens in separate window
- [x] Links in About dialog work
- [x] Documentation is accurate and helpful
- [ ] Works on Windows, macOS, and Linux — see tests/manual/help.md
- [x] Help is easy to navigate