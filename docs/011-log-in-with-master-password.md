# US-011: Log In with Master Password

## User Story

**As a** user  
**I want to** log in with my master password  
**So that** I can access my encrypted data

## Priority

**MVP:** Must Have

**Rationale:** Every time the user starts OurCRM, they need to authenticate to unlock the encrypted database. This is the primary authentication mechanism.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 2 hours: Create login UI
- 2 hours: Implement password verification with Argon2id
- 1 hour: Implement exponential backoff for failed attempts
- 2 hours: Create Result objects for authentication outcomes
- 2 hours: Write tests for login flow
- 2 hours: Test cross-platform behavior
- 1 hour: Add logging for login attempts

## Dependencies

**Depends on:** US-010 (Create Master Password), US-014 (Encrypted Database)

**Blocks:** US-002 (Run Application - requires authentication), all user features

## Description

When a user starts OurCRM, they should be prompted to enter their master password. The password is verified using Argon2id, which takes approximately 2 seconds. If the password is correct, the encrypted database is unlocked and the user can access their data. If incorrect, the user must wait an increasing amount of time before trying again (exponential backoff).

The login screen should be simple and clear, with a password field and a submit button. Failed attempts should be logged for security purposes. After successful login, the user should see the main application window.

## Acceptance Criteria

- [x] User can log in with correct master password
- [x] Incorrect password shows clear error message
- [x] Failed login attempts trigger exponential backoff
- [x] Wait time doubles after each failure (2s, 4s, 8s, 16s, etc.)
- [x] Successful login resets the failure count
- [x] Password field masks the input
- [x] Password is not stored or logged in plain text
- [x] Verification takes approximately 2 seconds
- [x] Login attempt is logged (success or failure)
- [ ] Works on Windows, macOS, and Linux — see tests/manual/authentication.md
- [x] Clear UI with password field and submit button
- [x] Cannot proceed with empty password
- [x] Database is unlocked after successful login