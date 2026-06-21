# US-012: Generate Recovery Password

## User Story

**As a** user  
**I want to** see a recovery password during setup  
**So that** I can recover my data if I forget my master password

## Priority

**MVP:** Must Have

**Rationale:** Users forget passwords. Without a recovery mechanism, all data would be permanently inaccessible. The recovery password is a critical safety mechanism.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Implement cryptographically secure random number generation
- 2 hours: Create recovery password generator (32 characters)
- 2 hours: Format password for display (with dashes for readability)
- 2 hours: Create UI to display the recovery password
- 1 hour: Add "Copy to Clipboard" functionality
- 1 hour: Implement secure display (clear from screen after confirmation)
- 2 hours: Write tests for generation and formatting
- 1 hour: Document the recovery process

## Dependencies

**Depends on:** US-010 (Create Master Password)

**Blocks:** US-013 (Confirm Recovery Password Saved), US-019 (Recover from Master Password)

## Description

During setup, after creating the master password, the system generates a cryptographically random 32-character recovery password. This password is displayed to the user once and only once. The user must save this password in a secure location (password manager, safe, etc.) because it will be needed if they ever forget their master password.

The recovery password uses a secure character set that excludes ambiguous characters (0, O, I, l, 1) to make it easier to read and write down correctly. The password is formatted with dashes every 5 characters to improve readability.

## Acceptance Criteria

- [x] Recovery password is 32 characters long
- [x] Uses cryptographically secure random generation
- [x] Excludes ambiguous characters (0, O, I, l, 1)
- [x] Formatted with dashes every 5 characters
- [x] Displayed clearly during setup
- [x] Can be copied to clipboard
- [x] Shown only once
- [x] Not stored in plain text anywhere
- [x] Different each time it's generated
- [x] Contains mix of character types
- [ ] Works on Windows, macOS, and Linux — see tests/manual/authentication.md
- [x] UI clearly warns this is the only time it will be shown