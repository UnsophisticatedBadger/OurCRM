# View Call List — Manual Tests

**Story:** [US-017 — View Call List](../../../docs/017-view-call-list.md)

## Call list opens and shows contacts sorted by priority

1. Add several contacts with different states: one overdue callback, one with a callback due today, one with a callback due later this week, one new contact with no callback set, and one marked Not Interested
2. Open the call list view
3. Confirm overdue callbacks appear first, followed by due-today callbacks, then due-this-week callbacks, then new contacts
4. Confirm the Not Interested contact does not appear in the list

## Each row shows the expected fields

1. Open the call list with at least one contact visible
2. Confirm each row displays: contact name, phone number, property address, and next callback date (or "New" if no callback set)

## Empty state when no contacts exist

1. Open the app with no contacts added
2. Open the call list view
3. Confirm an appropriate empty state message is shown rather than a blank screen
