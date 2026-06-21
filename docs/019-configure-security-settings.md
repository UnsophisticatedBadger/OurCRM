# US-019: Configure Security Settings

## User Story

**As a** user  
**I want to** configure security settings  
**So that** I can protect my data and control authentication behavior

## Priority

**MVP:** Must Have

**Rationale:** Security settings allow users to configure auto-lock, failed login attempt handling, and other security-related options. These are critical for protecting user data.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Identify security settings to include
- 2 hours: Create UI for each setting
- 1 hour: Implement auto-lock timeout
- 1 hour: Implement session management
- 1 hour: Add validation
- 1 hour: Test immediate vs restart-required changes
- 2 hours: Test all settings work correctly
- 1 hour: Test settings persistence

## Dependencies

**Depends on:** US-017 (Open Settings Window)

**Blocks:** US-020 (Create Contact - requires security foundation)

## Description

The Security settings category allows users to configure security-related options including auto-lock timeout, session management, and failed login attempt handling. These settings control how OurCRM protects user data and responds to potential security threats.

Settings should be loaded when the Settings window opens, and saved when the user clicks "Save". Some settings take effect immediately, while others may require an application restart. The UI should clearly indicate which settings require a restart.

## Acceptance Criteria

- [x] Security settings category is accessible
- [x] Auto-lock timeout can be configured
- [x] Auto-lock can be set to Never
- [x] Auto-lock takes effect immediately
- [x] Auto-lock resets on user activity
- [x] Auto-lock triggers after inactivity
- [x] Settings persist across application restarts
- [x] Settings are validated before saving
- [x] Default values are sensible
- [x] Failed login backoff is documented
- [ ] Works on Windows, macOS, and Linux — see tests/manual/app-shell.md
- [x] Configuration is stored in TOML format