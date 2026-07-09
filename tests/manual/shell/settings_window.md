# Open the Settings Window — Manual Tests

**Story:** [#11 — Open the Settings Window](../../docs/11-open-settings-window.md)

## Smoke Test: Sidebar Click-Through

Automated coverage drives navigation to Settings programmatically
(`main_window.navigate_to(...)`), which exercises the real signal chain but never
simulates an actual mouse click on the "Settings" sidebar item — same gap as #10's
navigation testing. This is the only place that proves clicking Settings in the
sidebar actually works for a real user.

### User clicks Settings in the sidebar

1. Run `uv run ourcrm` and log in
2. Click "Settings" in the sidebar
3. Confirm the Settings window appears with a category list on the left (General, Security, AI, MLS, Email, Calendar, Notifications) and Save/Cancel buttons at the bottom

## User opens Settings from every entry point

1. Log in (Dashboard is shown by default)
2. Click File > Settings — confirm the Settings window appears
3. Close Settings, then press Ctrl+, (Ctrl and the comma key) — confirm the Settings window appears
4. Close Settings, click "Contacts" in the sidebar, then click "Settings" in the sidebar — confirm it still opens correctly from a non-default section

## User saves and cancels changes

1. Open Settings (any entry point) and confirm General is selected by default
2. Change the Theme dropdown to "Dark"
3. Click Save
4. Confirm the app's theme visibly changes to dark
5. Close and reopen Settings — confirm the Theme dropdown still shows "Dark"
6. Change the Theme dropdown to "Light"
7. Click Cancel instead of Save
8. Reopen Settings — confirm the Theme dropdown still shows "Dark" (the cancelled change was discarded, not persisted)
