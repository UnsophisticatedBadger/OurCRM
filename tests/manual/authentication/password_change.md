# Change Master Password — Manual Tests

**Story:** [#8 — Change Master Password](../../docs/8-change-master-password.md)

## User finds Change Master Password in Security Settings
1. Log in and navigate to Settings → Security
2. Confirm a "Change Master Password" button is present
3. Click it — confirm the Change Master Password dialog opens with a current password field, a new password field (with a "Show" toggle button), and a confirm field (with no toggle)

## User types a new password and watches the requirement checklist update live
1. Open the Change Master Password dialog
2. Confirm all 5 requirement labels under the new password field, and the "Passwords match" label under the confirm field, start in red
3. Type a new password one character at a time and confirm each requirement label turns green individually as it is satisfied (not all at once)
4. Click "Show" next to the new password field — confirm the password becomes readable plain text and the button now reads "Hide"; click it again — confirm it re-masks
5. Enter a value in the confirm field that does not match — confirm the "Passwords match" label stays red
6. Correct the confirm field to match — confirm the "Passwords match" label turns green

## User enters the wrong current password and is denied
1. Open the Change Master Password dialog
2. Enter an incorrect current password, a valid new password, and a matching confirmation
3. Click Continue
4. Confirm an "Incorrect current password" error is shown and the dialog stays open

## User enters a new password that is too short
1. Open the Change Master Password dialog
2. Enter the correct current password and a new password shorter than 12 characters (with matching confirmation)
3. Confirm the length requirement label stays red and the change is not accepted

## User enters a new password that does not match its confirmation
1. Open the Change Master Password dialog
2. Enter the correct current password and a valid new password
3. Enter a different value in the confirm field
4. Confirm the "Passwords match" label stays red and the change is not accepted

## User successfully changes the password and is logged out
1. Open the Change Master Password dialog
2. Enter the correct current password and a valid new password that matches its confirmation
3. Click Continue
4. Confirm the app returns to the login screen

## Old password is rejected after the change; new password and data still work
1. After changing the password, attempt to log in with the old password
2. Confirm it is rejected
3. Log in with the new password
4. Confirm all contacts, leads, and other data are intact
