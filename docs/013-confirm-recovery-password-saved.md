# US-013: Confirm Recovery Password Saved

## User Story

**As a** user  
**I want to** confirm that I have saved the recovery password  
**So that** I don't lose access to my data if I forget my master password

## Priority

**MVP:** Must Have

**Rationale:** Users often skip important warnings. Requiring explicit confirmation ensures they understand the importance of saving the recovery password before proceeding.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 2 hours: Create confirmation UI with checkboxes
- 1 hour: Implement three-step confirmation process
- 1 hour: Add visual warnings and emphasis
- 1 hour: Prevent proceeding without confirmation
- 1 hour: Add "Show password again" option (optional)
- 1 hour: Test confirmation flow
- 1 hour: Test cancellation behavior

## Dependencies

**Depends on:** US-012 (Generate Recovery Password)

**Blocks:** US-014 (Encrypted Database - needs setup completion), US-019 (Recover from Master Password)

## Description

After the recovery password is displayed, the user must explicitly confirm that they have saved it before proceeding with setup. This confirmation uses a three-step process where the user must type specific words to ensure they are paying attention and have actually saved the password.

The confirmation requires:
1. Checking a box: "I have written down or saved the master recovery password"
2. Checking a box: "I understand I cannot recover my data without this"
3. Typing "CONFIRM" to finalize

The UI should make it clear that this is a critical step and that proceeding without saving the password could result in permanent data loss. If the user cancels, the setup should not continue.

## Acceptance Criteria

- [x] User must check first checkbox to proceed
- [x] User must check second checkbox to proceed
- [x] User must type "CONFIRM" exactly to proceed
- [x] Continue button is disabled until all confirmations are complete
- [x] Visual warnings are prominent and clear
- [x] Consequences of not saving are clearly stated
- [x] User can cancel setup from this screen
- [x] Cancellation prevents any data from being saved
- [x] Confirmation is logged for security purposes
- [ ] Works on Windows, macOS, and Linux — see tests/manual/authentication.md
- [x] UI makes the importance of this step clear
- [x] Difficult to accidentally skip the confirmation