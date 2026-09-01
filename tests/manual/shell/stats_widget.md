# Dashboard Stats Widget — Manual Tests

**Story:** [#20 — Dashboard Stats Widget](../../../docs/20-dashboard-stats-widget.md)

## User sees four stat tiles on the dashboard with no data entered
1. Launch the app with a fresh, empty database and land on the Dashboard
2. Confirm four tiles are visible: Contacts, Active Leads, Properties, Due Today
3. Confirm every tile shows "0"

## Dashboard shows the real contact and lead counts
1. Create 2 contacts and 1 lead
2. Navigate to the Dashboard (or return to it if already there)
3. Confirm the Contacts tile shows "2" and the Active Leads tile shows "1"

## Dashboard shows the real due-today count
1. Log a "Call Back" outcome on a contact with the callback due today
2. Navigate to the Dashboard
3. Confirm the Due Today tile shows the contact

## Properties tile always shows 0
1. With any amount of CRM data entered, view the Dashboard
2. Confirm the Properties tile always shows "0" — there is no Properties capability yet, so this is a placeholder

## Dashboard refreshes every time it is shown, not just at launch
1. Note the Contacts tile's count on the Dashboard
2. Navigate away to another section and create a new contact
3. Navigate back to the Dashboard
4. Confirm the Contacts tile count increased without restarting the app
