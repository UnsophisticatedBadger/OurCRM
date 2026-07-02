# Recovery Password Setup — Manual Tests

**Story:** [#4 — Set Up Recovery Password](../../docs/4-generate-recovery-password.md)

## User sees their recovery password after creating a master password

1. Delete any existing `ourcrm.db` and run `uv run ourcrm`
2. Create a master password (see `password_creation.md`)
3. Confirm the recovery password setup screen appears immediately after, before the main window
4. Confirm the displayed recovery password is 32 characters, grouped with dashes every 5 characters, with no ambiguous characters (0, O, I, l, 1)
5. Click "Copy to Clipboard" and paste into a text editor — confirm it matches the displayed password with the dashes removed

## User must confirm before proceeding

1. On the recovery password setup screen, confirm the Continue button starts disabled
2. Check only the first checkbox — confirm Continue stays disabled
3. Check only the second checkbox — confirm Continue stays disabled
4. Check both checkboxes and type "confirm" (lowercase) — confirm Continue stays disabled
5. Change the text to "CONFIRM" exactly — confirm Continue becomes enabled
6. Click Continue — confirm the main window opens

## User closes the setup screen before confirming

1. Delete any existing `ourcrm.db` and run `uv run ourcrm`
2. Create a master password and reach the recovery password setup screen
3. Click the X on the setup screen
4. Confirm a warning explains that the master password and database will be deleted if you proceed
5. Choose to stay — confirm the setup screen is still open and nothing was deleted
6. Click the X again and choose to exit — confirm the application closes
7. Confirm the `ourcrm.db` file no longer exists in the data directory
8. Run `uv run ourcrm` again — confirm it starts fresh in create-password mode (no leftover master password)
