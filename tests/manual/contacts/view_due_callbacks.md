# View Due Callbacks — Manual Tests

**Story:** [#47 — View Due Callbacks](../../../docs/47-view-due-callbacks.md)

## Filtering to just this week's callbacks
1. Open the Call List with a mix of contacts: some with overdue callbacks, some due this week, some with no callback set
2. Check "Show only callbacks due this week"
3. Confirm only the overdue/due-today/due-this-week contacts remain visible
4. Uncheck the filter and confirm the full call list returns

## Overdue callbacks are highlighted
1. Arrange a contact with an overdue callback
2. Open the Call List
3. Confirm the row has a red tint and an "⚠ Overdue" badge on the contact's name

## Relative day counts display correctly
1. Arrange contacts with an overdue callback, a callback due today, and a callback due later this week
2. Open the Call List
3. Confirm each shows the correct relative text: "N days overdue", "due today", or "due in N days"
