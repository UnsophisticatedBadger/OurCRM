# Dashboard — Manual Tests

**Story:** [US-018 — Dashboard](../../../docs/018-dashboard.md)

## Dashboard is the first screen shown after login

1. Log in with the master password
2. Verify the dashboard is displayed immediately — no additional navigation required

## Due callbacks appear in the Call Back Today section

1. Add a contact with a callback timeframe that is due today or overdue
2. Log in or return to the dashboard
3. Verify the contact appears in the "Call Back Today" section
4. Verify contacts are sorted by how overdue they are — most overdue first

## New contacts appear in the New to Call section

1. Add a contact to the call list without logging an outcome
2. Return to the dashboard
3. Verify the contact appears in the "New to Call" section
4. Verify contacts are sorted by date added — most recent first

## Contact details are visible on the dashboard

1. Open the dashboard
2. Verify each contact in both sections shows name, phone number, and property address

## Call button appears on dashboard contacts when calling is configured

1. Configure Google Voice in Settings
2. Open the dashboard
3. Verify each contact shows a Call button

## Call count updates after logging an outcome

1. Open the dashboard and note the calls-logged-today count
2. Open a contact from the dashboard and log a call outcome
3. Return to the dashboard
4. Verify the count has increased by one

## Clicking a contact opens their detail view

1. Click a contact on the dashboard
2. Verify the contact detail view opens
3. Verify the outcome can be logged from that view
