# Set Callback Timeframe — Manual Tests

**Story:** [US-019 — Set Callback Timeframe](../../../docs/019-set-callback-timeframe.md)

## Callback timeframe picker appears after selecting Call Back

1. Open the call list and select a contact
2. Choose the "Call Back" outcome
3. Confirm a timeframe picker appears before the outcome is confirmed
4. Confirm the options shown are: This Week, Next Week, In Two Weeks, This Month

## Selecting a timeframe removes the contact from the active call list

1. Choose "Call Back" and select "Next Week"
2. Confirm the contact no longer appears in the active call list
3. Confirm the contact is not deleted — it exists in the system with a callback scheduled

## Contact reappears when the timeframe arrives

1. Set a callback for "This Week" (or simulate a date change to the target week)
2. Confirm the contact reappears in the call list sorted above new contacts

## Cancelling the timeframe picker does not save the outcome

1. Choose "Call Back"
2. When the timeframe picker appears, dismiss or cancel it
3. Confirm no outcome is saved and the contact remains in the active list unchanged
