# US-128: Password Recovery Using Recovery Password

## User Story

**As a** user  
**I want to** recover access using my recovery password if I forget my master password  
**So that** I don't lose all my data if I forget my master password

## Priority

**MVP:** Must Have

**Rationale:** Users forget passwords. Without a recovery mechanism, all data would be permanently inaccessible. The recovery password generated during setup (US-012) must actually work to recover access. This is critical for user trust and data safety.

## Estimated Effort

**Size:** Medium (M) - 3-5 days

**Breakdown:**
- 2 hours: Design recovery flow UI
- 3 hours: Implement recovery password verification
- 4 hours: Implement password reset with recovery
- 3 hours: Implement database re-encryption with new password
- 2 hours: Add recovery attempt logging
- 2 hours: Test recovery flow
- 2 hours: Test on all platforms

## Dependencies

**Depends on:** US-010 (Create Master Password), US-012 (Generate Recovery Password), US-014 (Create Encrypted Database)

**Blocks:** None

## Description

When a user forgets their master password, they should be able to use the recovery password (generated during setup) to regain access. The recovery process:
1. User clicks "Forgot Password?" on login screen
2. User enters the recovery password
3. System verifies the recovery password
4. User creates a new master password
5. Database is re-encrypted with new password
6. User can log in with new password

The recovery password is stored as a hash (not plain text) and is separate from the master password. It should only be usable for recovery, not for normal login.

## Acceptance Criteria

- [x] "Forgot Password?" link on login screen
- [x] Recovery password verification works
- [x] Recovery password is case-sensitive
- [x] New password must meet all requirements
- [x] New password must be confirmed
- [x] Database is re-encrypted with new password
- [x] User can log in with new password immediately
- [x] All data remains accessible after recovery
- [ ] Recovery attempts are logged — **deferred to US-169 (Security Event Logging)**
- [x] Recovery password can be used multiple times
- [x] Error messages don't reveal if recovery password exists
- [x] Recovery flow is secure and atomic
- [ ] Works on Windows, macOS, and Linux — see tests/manual/authentication.md
- [x] Clear instructions throughout the flow