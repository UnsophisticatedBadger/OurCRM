# View Due Callbacks — Manual Tests

**Story:** [US-020 — View Due Callbacks](../../../docs/020-view-due-callbacks.md)

## Due This Week filter shows only callbacks due this week

1. Add contacts with callbacks set for: this week, next week, and overdue (past week)
2. Apply the "Due This Week" filter on the call list
3. Confirm only contacts with callbacks due this week or overdue are shown
4. Confirm contacts with callbacks scheduled for next week are hidden

## Overdue callbacks appear first and are highlighted

1. Ensure at least one contact has a callback that is past due and one is due later this week
2. Open the "Due This Week" filtered view
3. Confirm overdue contacts appear above upcoming-this-week contacts
4. Confirm overdue contacts are visually highlighted (e.g. different color or icon)

## Days overdue and days remaining are displayed

1. Open the "Due This Week" filtered view
2. For an overdue contact, confirm the row shows how many days overdue (e.g. "2 days overdue")
3. For a contact due in the future, confirm the row shows days remaining (e.g. "Due in 3 days")

## Clearing the filter returns to the full call list

1. Apply the "Due This Week" filter
2. Clear or remove the filter
3. Confirm the full call list reappears with all contacts in their normal sort order
