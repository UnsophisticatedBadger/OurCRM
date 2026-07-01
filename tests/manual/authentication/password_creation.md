# Master Password Creation — Manual Tests

**Story:** [#3 — Create Master Password](../../docs/3-create-master-password.md)

## User cold-launches from a fresh install and creates a password

1. Delete any existing `ourcrm.db` from the data directory
2. Run `uv run ourcrm`
3. Confirm the "Create Master Password" dialog appears before the main window, with a password field (with a "Show" toggle button) and a confirmation field (with no toggle)
4. Confirm all 5 requirement labels under the password field, and the "Passwords match" label under the confirmation field, start in red
5. Type a password one character at a time and confirm each requirement label turns green individually as it is satisfied (not all at once)
6. Click "Show" next to the password field — confirm the password becomes readable plain text and the button now reads "Hide"; click it again — confirm it re-masks
7. Enter a password shorter than 12 characters (matching confirmation) — confirm the length error is shown, and the length requirement label remains red
8. Enter a valid password with a different value in the confirmation field — confirm "Passwords do not match" is shown and the "Passwords match" label is red
9. Correct the confirmation field to match — confirm the "Passwords match" label turns green
10. Click Create
11. Confirm the main window opens
12. Confirm a `ourcrm.db` file exists in the data directory

## User closes the create-password dialog and the application exits

1. Delete any existing `ourcrm.db`
2. Run `uv run ourcrm`
3. Click the X on the startup dialog
4. Confirm the application exits and no DB file was created
