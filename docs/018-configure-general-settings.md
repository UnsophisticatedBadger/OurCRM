# US-018: Configure General Settings

## User Story

**As a** user  
**I want to** configure general application settings  
**So that** I can customize OurCRM to match my preferences

## Priority

**MVP:** Must Have

**Rationale:** General settings are the most frequently accessed settings and affect the daily user experience. Users need to be able to configure these without diving into complex configuration files.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Identify which settings go in General
- 2 hours: Create UI for each setting
- 2 hours: Implement save/load logic
- 1 hour: Add validation
- 1 hour: Implement immediate vs restart-required changes
- 2 hours: Test all settings work correctly
- 1 hour: Test settings persistence
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-017 (Open Settings Window)

**Blocks:** All other settings categories (Security, AI, MLS, etc.)

## Description

The General settings category includes application-wide preferences that don't fit into more specific categories. This includes theme selection (light/dark/auto), language preferences, date format, time format, default views, and other common preferences.

Settings should be loaded when the Settings window opens, and saved when the user clicks "Save". Some settings take effect immediately (like theme), while others may require an application restart. The UI should clearly indicate which settings require a restart.

## Acceptance Criteria

- [x] General settings category is accessible
- [x] Theme can be changed (Light/Dark/Auto)
- [x] Theme changes take effect immediately
- [x] Date format can be configured
- [x] Time format can be configured (12-hour/24-hour)
- [x] Settings persist across application restarts
- [x] Settings are validated before saving
- [x] Default values are sensible
- [x] Settings requiring restart are clearly indicated
- [x] Changes take effect immediately when possible
- [ ] Works on Windows, macOS, and Linux — see tests/manual/app-shell.md
- [x] Configuration is stored in TOML format
- [ ] Settings can be reset to defaults (if implemented)