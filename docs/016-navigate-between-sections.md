# US-016: Navigate Between Sections

## User Story

**As a** user  
**I want to** navigate between different sections of the application  
**So that** I can access contacts, leads, properties, and other features

## Priority

**MVP:** Must Have

**Rationale:** OurCRM has multiple major sections (contacts, leads, properties, transactions, etc.). Users need an intuitive way to navigate between them without getting lost or confused.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 2 hours: Design navigation pattern (sidebar, tabs, or menu)
- 3 hours: Implement navigation UI
- 2 hours: Create section switching logic
- 1 hour: Add visual indicators for current section
- 2 hours: Implement keyboard shortcuts for navigation
- 1 hour: Add navigation history/back button
- 2 hours: Test navigation flow
- 1 hour: Test accessibility (keyboard navigation)

## Dependencies

**Depends on:** US-015 (Create the First Window)

**Blocks:** US-020 (Create Contact), US-030 (Create Lead), US-040 (Create Property), all section-specific features

## Description

The main window should provide clear navigation between major sections of OurCRM. This includes Contacts, Leads, Properties, Transactions, Calendar, and Settings. The navigation should be intuitive, consistent, and accessible.

Users should be able to:
- See all available sections at a glance
- Know which section they're currently in
- Switch between sections quickly
- Use keyboard shortcuts for common sections
- Navigate back to previous sections if needed

The navigation pattern should be familiar to users (sidebar navigation is common in modern desktop apps) and should not interfere with the main content area.

## Acceptance Criteria

- [x] All major sections are accessible from navigation
- [x] Current section is visually indicated
- [x] Keyboard shortcuts work for common sections
- [x] Navigation is keyboard accessible
- [x] Navigation is fast and responsive
- [ ] Works on Windows, macOS, and Linux — see tests/manual/app-shell.md
- [ ] Platform-specific keyboard shortcuts (Ctrl vs Cmd) — see tests/manual/app-shell.md
- [x] Navigation is intuitive for new users
- [x] All sections load correctly
- [x] No lag or performance issues
- [x] Navigation pattern follows platform conventions