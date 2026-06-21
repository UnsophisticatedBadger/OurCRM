# US-017: Open Settings Window

## User Story

**As a** user  
**I want to** open the Settings window  
**So that** I can configure application preferences and options

## Priority

**MVP:** Must Have

**Rationale:** Users need to be able to configure the application to match their preferences and workflow. Settings include theme, notifications, auto-lock, AI provider, MLS configuration, and more.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 2 hours: Design settings window layout
- 3 hours: Create settings UI with categories
- 2 hours: Implement settings categories (General, Security, Integrations, etc.)
- 2 hours: Add navigation within settings
- 1 hour: Implement save/cancel functionality
- 1 hour: Add validation for settings
- 1 hour: Test settings persistence
- 2 hours: Test all settings categories

## Dependencies

**Depends on:** US-015 (Create the First Window), US-016 (Navigate Between Sections)

**Blocks:** US-018 (Configure General Settings), US-021 (View Contact List), all configuration features

## Description

The Settings window allows users to configure all aspects of OurCRM. The window should be organized into logical categories (General, Security, AI, MLS, Email, Calendar, Notifications, About) with a navigation panel on the left and settings content on the right.

Settings should be saved when the user clicks "Save" or "OK", and changes should be applied immediately or on next restart as appropriate. The Settings window should be modal or modeless (user's choice), and should remember its size and position.

## Acceptance Criteria

- [x] Settings window opens from multiple entry points
- [x] All settings categories are accessible
- [x] Navigation between categories works
- [x] Save button saves changes
- [x] Cancel button discards changes
- [x] Close button prompts to save if changes were made
- [x] Settings are validated before saving
- [x] Settings persist across application restarts
- [x] Window remembers size and position
- [x] Keyboard shortcuts work (Ctrl+, / Cmd+,)
- [ ] Works on Windows, macOS, and Linux — see tests/manual/app-shell.md
- [x] Settings categories are clearly organized
- [x] UI is intuitive and easy to navigate