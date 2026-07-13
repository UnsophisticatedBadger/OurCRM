# Password Recovery Flow — Manual Tests

**Story:** [#9 — Password Recovery Flow](../../docs/9-password-recovery-flow.md)

### Forgot Password link is present at both entry points
1. Launch the app fresh (DB file exists from prior setup) and confirm a "Forgot Password?" link is visible on the startup "Enter Master Password" dialog
2. Log in, then log out via File > Logout, and confirm the same link is visible on the post-logout login screen

### Wrong recovery password is rejected
1. Click "Forgot Password?"
2. Enter an incorrect recovery password
3. Confirm the error "Incorrect recovery password" is shown and the form stays open

### Case-mismatched recovery password is rejected identically
1. Click "Forgot Password?"
2. Enter the correct recovery password but with different letter casing (e.g. lowercase where the saved password has uppercase)
3. Confirm the same "Incorrect recovery password" error is shown, not a different message

### Correct recovery password proceeds to new password screen
1. Enter the correct recovery password (saved from #4 setup)
2. Confirm a form to set a new master password is shown
3. Enter a new password shorter than 12 characters and confirm it is rejected with a validation error
4. Enter a valid new password and mismatched confirmation and confirm it is rejected
5. Enter a valid, matching new password and confirm it is accepted

### User enters an incorrect recovery password three times in a row and watches the wait double
1. Click "Forgot Password?"
2. Enter an incorrect recovery password and click Verify — confirm the form stays open with no lockout yet
3. Enter an incorrect recovery password a second time — confirm the form stays open with no lockout yet
4. Enter an incorrect recovery password a third time — confirm the error reads "Incorrect recovery password. Please wait 30 seconds before trying again." and Verify is greyed out
5. Wait for Verify to re-enable, then enter an incorrect recovery password again — confirm the wait is now 60 seconds
6. Enter the correct recovery password and confirm the flow proceeds normally

### Successful recovery logs in automatically and issues a new recovery password
1. Complete the recovery flow with a valid new password
2. Confirm the app logs in automatically without a separate login step
3. Confirm a new recovery password is shown and attempting to close the screen without checking both confirmation boxes and typing "CONFIRM" keeps it open
4. Check both boxes, type "CONFIRM", and confirm the app becomes accessible

### Old credentials are invalidated
1. After recovery, log out and attempt to log in with the old master password
2. Confirm it is rejected
3. Log in with the new master password and confirm all data (contacts, leads, etc. saved before recovery) is intact
4. Click "Forgot Password?" again and attempt recovery with the *old* recovery password
5. Confirm it is rejected with "Incorrect recovery password"
