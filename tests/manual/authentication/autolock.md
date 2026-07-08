# Auto-Lock After Inactivity — Manual Tests

**Story:** [#7 — Auto-Lock After Inactivity](../../docs/7-autolock-after-inactivity.md)

## Smoke Test: App Startup Wiring

### Auto-lock actually runs when the app is launched normally

1. Launch the app with `uv run ourcrm` and log in
2. Do not touch the keyboard or mouse
3. Confirm the lock screen appears within 30 seconds

*Regression guard for the wiring in `main.py` — `auto_lock_timeout_seconds=30` must
be passed to `MainWindow` at startup or auto-lock silently never runs, even though
every automated test passes (the tests construct `MainWindow` directly and bypass
`main.py` entirely).*

## User logs in and waits 30 seconds without touching the keyboard or mouse

1. Launch the app with `uv run ourcrm` and log in with the correct master password
2. Note the section you're viewing (e.g. Dashboard)
3. Do not touch the keyboard or mouse for at least 30 seconds
4. Confirm the lock screen appears, showing the "OurCRM" branding, a password field, and an "Unlock" button

## User moves the mouse before 30 seconds and the lock is deferred

1. Log in
2. After about 20 seconds of no input, move the mouse or press a key
3. Wait another 20 seconds without further input
4. Confirm the lock screen does not appear until a full 30 seconds have passed since the last activity

## User enters the correct password on the lock screen

1. Log in, navigate to a non-default section (e.g. Contacts), then wait for the lock screen to appear
2. Enter the correct master password and click Unlock
3. Confirm the lock screen disappears and the Contacts section is shown, exactly as it was before locking

## User enters the wrong password on the lock screen

1. Log in and wait for the lock screen to appear
2. Enter an incorrect password and click Unlock
3. Confirm an error message is shown and the lock screen remains open
4. Enter the correct password and confirm the lock screen disappears
