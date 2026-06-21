# US-010: Create Master Password

## User Story

**As a** user  
**I want to** create a master password during setup  
**So that** my data is secure and only I can access it

## Priority

**MVP:** Must Have

**Rationale:** Security is fundamental to the application. The master password protects the encrypted database and all user data. Without it, we cannot meet our security commitments.

## Estimated Effort

**Size:** Medium (M) - 3-5 days

**Breakdown:**
- 2 hours: Design password requirements
- 3 hours: Create password validation logic
- 4 hours: Create setup wizard UI for password creation
- 2 hours: Implement password strength meter
- 3 hours: Hash password with Argon2id
- 2 hours: Store password hash securely
- 2 hours: Write tests for validation
- 2 hours: Test cross-platform behavior

## Dependencies

**Depends on:** US-008 (Create First Test), US-020 (Create Contact - needs security)

**Blocks:** US-011 (Log In), US-012 (Recovery Password), US-013 (Confirm Recovery Password)

## Description

During the initial setup of OurCRM, a user must create a master password. This password must be at least 12 characters long and include uppercase, lowercase, numbers, and special characters. The password should be hashed using Argon2id with parameters calibrated to take approximately 2 seconds to verify.

The user will type this password every time they start OurCRM. It protects the encrypted database and all stored credentials. The password is never stored in plain text - only the Argon2id hash is stored in the OS keyring.

## Acceptance Criteria

- [x] User can create a master password during setup
- [x] Password must be at least 12 characters
- [x] Password must include uppercase, lowercase, numbers, and special characters
- [x] Password is hashed with Argon2id
- [x] Hash is stored in OS keyring
- [x] Original password is never stored
- [x] Password strength meter works
- [x] Confirmation field validates match
- [x] Clear error messages for all validation failures
- [x] Verification takes approximately 2 seconds
- [ ] Works on Windows, macOS, and Linux — see tests/manual/authentication.md
- [x] Password requirements are clearly documented