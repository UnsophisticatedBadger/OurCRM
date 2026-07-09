# Configure Security Settings — Manual Tests

**Story:** [#13 — Configure Security Settings](../../docs/13-configure-security-settings.md)

## User views the Security settings

1. Run `uv run ourcrm` and log in
2. Open Settings (any entry point) and click "Security" in the category list
3. Confirm an "Auto-lock Timeout" field is shown, displaying minutes with a "Never" option at 0

## User changes the auto-lock timeout and it takes effect immediately, without restarting

Automated tests confirm the running app reconfigures its live auto-lock timer as soon
as Settings is saved, but this is the only check that a real user, in a single running
session, actually experiences that — no restart required.

1. Run `uv run ourcrm` and log in
2. Open Settings > Security, set Auto-lock Timeout to "1" minute, click Save
3. Stay in the same session — do not close or relaunch the app
4. Stop touching the mouse/keyboard and wait about a minute — confirm the app locks and shows the lock screen
5. Unlock with the master password

## User sets auto-lock to Never and it stops locking immediately

1. With the app still running from the previous test, open Settings > Security, set Auto-lock Timeout to "0" (displays as "Never"), click Save
2. Stay in the same session — do not close or relaunch the app
3. Leave the app idle for several minutes — confirm it does not lock

## Settings persist across restarts

1. Open Settings > Security, set Auto-lock Timeout to "5" minutes, click Save
2. Close and relaunch OurCRM, log in
3. Open Settings > Security — confirm the field still shows "5" minutes

---

Note: save-failure error handling (disk write errors) is covered by automated tests
only — it's impractical to reliably simulate a disk failure through the running app.
