# Navigate Between Sections — Manual Tests

**Story:** [#10 — Navigate Between Sections](../../docs/10-navigate-between-sections.md)

## Smoke Test: Sidebar Click-Through

Automated coverage drives navigation programmatically (`main_window.navigate_to(...)`),
which exercises the real signal chain from the nav panel to the content area but never
simulates an actual mouse click on a sidebar item. Qt's own click-to-select behavior on
the list widget is framework code, but this test is the only place that proves clicking
the sidebar actually works end-to-end for a real user.

### User clicks through every section in the sidebar

1. Run `uv run ourcrm` and log in
2. Click "Dashboard" in the sidebar — confirm the Dashboard page appears and "Dashboard" is highlighted
3. Click "Contacts" in the sidebar — confirm the Contacts page appears and "Contacts" is highlighted, and no other item stays highlighted
4. Click "Leads" in the sidebar — confirm the Leads page appears and is highlighted
5. Click "Properties" in the sidebar — confirm the Properties page appears and is highlighted
6. Click "Transactions" in the sidebar — confirm the Transactions page appears and is highlighted
7. Click "Calendar" in the sidebar — confirm the Calendar page appears and is highlighted
8. Click "Settings" in the sidebar — confirm the Settings page appears and is highlighted

## User navigates with keyboard shortcuts

1. Log in (Dashboard is shown by default)
2. Press Ctrl+2 — confirm the Contacts section becomes active
3. Press Ctrl+1 — confirm the Dashboard section becomes active again
4. Click "Leads" in the sidebar, then press Ctrl+1 — confirm the Dashboard section becomes active from a non-default starting point
