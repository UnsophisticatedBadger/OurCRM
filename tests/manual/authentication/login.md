# Log In and Out — Manual Tests

**Story:** [#6 — Log In and Out](../../docs/6-log-in-with-master-password.md)

## Smoke Test: App Startup Wiring

### File > Logout works when the app is launched normally

1. Launch the app with `uv run ourcrm`
2. Click File > Logout
3. Confirm the login screen appears

*Regression guard for the wiring in `main.py` — `auth_service` must be passed to
`MainWindow` at startup or Logout silently does nothing.*

### Packaged build stores its database in AppData, not the source tree

1. Build the packaged app (`uv run python scripts/build.py`) and launch
   `dist\ourcrm\ourcrm.exe` directly (not via `uv run`)
2. Create the master password and complete setup
3. Confirm `ourcrm.db` and `config.toml` appear under `%APPDATA%\ourcrm\`
4. Confirm no `ourcrm.db` was written into the project's `config\` folder

*Regression guard for `_is_frozen()` in `container.py` — Nuitka never sets
`sys.frozen`, so this must also check for its `__compiled__` module marker or
a packaged build silently uses the dev-mode source-relative path.*

## User re-launches after setup and enters correct password

1. Run `uv run ourcrm` (DB file exists from prior setup)
2. Confirm the "Enter Master Password" dialog appears
3. Enter the correct password and click Open
4. Confirm the main window opens

## User enters wrong password and retries

1. Run `uv run ourcrm`
2. Submit an incorrect password
3. Confirm an inline error appears and the dialog stays open
4. Submit the correct password
5. Confirm the main window opens

## User enters an incorrect password three times in a row and watches the wait double

1. Run `uv run ourcrm` (DB file exists from prior setup)
2. Enter an incorrect password and click Open
3. Confirm the error reads "Incorrect password. Please wait 2 seconds before trying again." and the Open button is greyed out
4. Wait for the Open button to re-enable, then enter an incorrect password again
5. Confirm the error reads "Incorrect password. Please wait 4 seconds before trying again." and the button is greyed out again
6. Wait for the Open button to re-enable, then enter an incorrect password a third time
7. Confirm the error reads "Incorrect password. Please wait 8 seconds before trying again." and the button is greyed out again
8. Wait out the final backoff, then enter the correct password
9. Confirm the main window opens

## User closes the login dialog — app exits cleanly

1. Run `uv run ourcrm`
2. Click the X on the startup dialog
3. Confirm the application exits without showing the main window

## User logs out via File menu and hands off the computer

1. Open the app with the correct password
2. Click File > Logout
3. Confirm the login screen appears and the main window is still visible behind it
4. Confirm no data is accessible without re-entering the password

## User logs back in after logout

1. Log out via File > Logout
2. Enter the correct password on the login screen
3. Confirm the Dashboard appears and the session resumes normally

## User enters wrong password on the login screen after logout

1. Log out via File > Logout
2. Submit an incorrect password on the login screen
3. Confirm an error message appears, the Login button is greyed out, and the login screen remains
