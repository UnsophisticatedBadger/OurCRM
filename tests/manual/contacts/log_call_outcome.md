# Log Call Outcome — Manual Tests

**Story:** [US-018 — Log Call Outcome](../../../docs/018-log-call-outcome.md)

## User logs a No Answer outcome

1. Open the call list and select a contact
2. Tap the call outcome button and choose "No Answer"
3. Confirm the outcome is saved with a timestamp
4. Confirm the contact remains in the call list

## User logs a Call Back outcome

1. Open the call list and select a contact
2. Choose "Call Back"
3. Confirm the callback timeframe picker appears (covered further in US-019 tests)
4. Select a timeframe and confirm
5. Confirm the contact moves out of the active call list

## User logs a Became Client outcome

1. Open the call list and select a contact
2. Choose "Became Client"
3. Confirm the contact displays a "Client" badge
4. Confirm the contact remains accessible but is visually distinguished

## User logs a Not Interested outcome

1. Open the call list and select a contact
2. Choose "Not Interested"
3. Confirm the contact disappears from the call list immediately
4. Confirm the contact still exists in the contacts database (not deleted)

## Call history is stored

1. Log multiple outcomes for the same contact over time
2. Open the contact detail view
3. Confirm all previous outcomes appear in the call history with timestamps
