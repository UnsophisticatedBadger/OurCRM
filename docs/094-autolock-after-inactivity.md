# US-094: Auto-Lock After Inactivity

## User Story

**As a** user  
**I want to** the app to automatically lock after a period of inactivity  
**So that** my data is protected if I walk away from my computer

## Priority

**MVP:** Must Have

**Rationale:** Auto-lock is a critical security feature. Without it, an unlocked application sitting idle is vulnerable to anyone with physical access to the computer. Auto-lock protects user data when the user steps away.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design auto-lock mechanism
- 1 hour: Implement activity tracking
- 1 hour: Implement inactivity timer
- 1 hour: Create lock screen
- 1 hour: Implement unlock flow
- 1 hour: Add settings for timeout duration
- 1 hour: Test auto-lock with various timeouts
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-019 (Configure Security Settings), US-011 (Log In with Master Password)

**Blocks:** US-095 (Change Master Password)

## Description

After a configured period of inactivity, the application should automatically lock, requiring the user to enter their master password to unlock it. The inactivity timer should reset on any user activity (keyboard, mouse, clicks).

The lock screen should be simple and secure, showing the OurCRM logo and a password field. The user can configure the timeout duration in settings (or disable auto-lock if they prefer, though this is less secure).

## Acceptance Criteria

- [x] Auto-lock triggers after configured inactivity period
- [x] Activity (keyboard, mouse) resets the timer
- [x] Lock screen is shown when locked
- [x] Lock screen has password field and unlock button
- [x] Correct password unlocks the app
- [x] Wrong password shows error and applies backoff
- [x] Auto-lock timeout is configurable in settings
- [x] Auto-lock can be disabled (with warning)
- [x] Lock screen is professional and secure
- [x] Unlock returns user to where they were
- [x] Settings persist across restarts
- [ ] Works on Windows, macOS, and Linux — see tests/manual/app-shell.md
- [x] Timer is accurate
- [x] No way to bypass without password
