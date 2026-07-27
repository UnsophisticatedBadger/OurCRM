# Set Callback Timeframe — Manual Tests

**Story:** [#46 — Set Callback Timeframe](../../../docs/46-set-callback-timeframe.md)

## Logging Call Back opens a timeframe picker
1. Open a contact from the call list and click Log Outcome
2. Select "Call Back"
3. Confirm a timeframe picker appears with options This Week, Next Week, In Two Weeks, and This Month

## Setting a callback removes the contact from the active call list
1. Log "Call Back" on a contact and choose "Next Week"
2. Confirm the contact disappears from the Call List view
3. Confirm the contact still appears in the All Contacts view

## A callback reappears in the call list once its window arrives
1. Log "Call Back" and choose "This Week" (a window that starts today)
2. Confirm the contact still appears in the Call List view with its callback due date shown
3. For a callback set with a later timeframe (e.g. "Next Week"), confirm it stays hidden from the Call List until its start date arrives, then reappears with its due date shown

## Call list priority order
1. Arrange several contacts with an overdue callback, a callback due today, a callback due this week, and no callback set
2. Open the Call List view
3. Confirm the order is: most overdue first, then due today, then due this week, then everyone else
