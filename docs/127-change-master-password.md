# US-127: Change Master Password

## User Story

**As a** user  
**I want to** change my master password  
**So that** I can update my credentials if I suspect compromise or want to improve security

## Priority

**MVP:** Must Have

**Rationale:** Users need the ability to change their master password for security reasons. This is a standard security feature expected in any application handling sensitive data. Without this, users are stuck with their initial password forever.

## Estimated Effort

**Size:** Medium (M) - 3-5 days

**Breakdown:**
- 2 hours: Design password change UI
- 3 hours: Implement password change form with validation
- 4 hours: Implement database re-encryption with new password
- 2 hours: Implement key derivation with new password
- 2 hours: Update OS keyring with new hash
- 2 hours: Test password change flow
- 2 hours: Test database re-encryption
- 2 hours: Test on all platforms

## Dependencies

**Depends on:** US-010 (Create Master Password), US-014 (Create Encrypted Database)

**Blocks:** None

## Description

Users should be able to change their master password from the Security settings. The process requires:
1. Entering the current password (verification)
2. Entering a new password (meeting all complexity requirements)
3. Confirming the new password
4. Re-encrypting the database with the new password
5. Updating the stored hash in the OS keyring

The database must be re-encrypted because the encryption key is derived from the master password. This is a sensitive operation that should be atomic (all or nothing) to prevent data corruption.

## Acceptance Criteria

- [x] "Change Master Password" option is in Security settings
- [x] Current password must be verified first
- [x] New password must meet all complexity requirements
- [x] New password must be confirmed
- [x] Database is re-encrypted with new password
- [x] New hash is stored in OS keyring
- [x] Old password no longer works
- [x] New password works immediately
- [x] Recovery password still works after change
- [x] Re-encryption is atomic (no corruption on failure)
- [x] Success message shown after change
- [x] Error messages are clear and helpful
- [ ] Works on Windows, macOS, and Linux — see tests/manual/authentication.md
- [x] All data remains accessible after change