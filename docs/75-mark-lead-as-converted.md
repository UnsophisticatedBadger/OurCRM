# 75 - Mark Lead As Converted

**Capability:** Leads
**Milestone:** MVP
**Status:** Not Done
**GitHub Issue:** #75

## User Story

As a real estate agent, I want to mark a lead as converted when they become a client, so that I can record the win, track my conversion history, and distinguish active leads from completed ones.

## Dependencies

- #65 — Move Lead Through Pipeline

## Acceptance Criteria

1. The lead details view shows a "Mark as Converted" button for any lead not already converted
2. Clicking it opens a confirmation dialog; the user must confirm before the conversion is recorded
3. Confirming records the conversion date on the lead and sets its pipeline stage to "Closed"
4. Converted leads are visually distinct in both the lead list and the pipeline view (e.g., a green indicator or checkmark)
5. Converting a lead shows a brief success notification
6. Changing a converted lead's stage to any other stage requires a second explicit confirmation

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/leads.feature`.

```gherkin
@story_75
Scenario: User marks a lead as converted and it moves to Closed
  Given the user is viewing a lead that has not been converted
  When the user clicks "Mark as Converted" and confirms
  Then the lead's pipeline stage is "Closed"
  And a success notification is shown

@story_75
Scenario: Conversion date is recorded on the lead
  Given the user converts a lead today
  When the user opens that lead's details
  Then the conversion date matches today's date

@story_75
Scenario: Converted lead is visually distinct in the list
  Given a lead has been marked as converted
  When the user views the lead list
  Then the converted lead has a green indicator distinguishing it from active leads

@story_75
Scenario: User cancels the conversion dialog and the lead is unchanged
  Given the user is viewing a lead
  When the user clicks "Mark as Converted" then cancels the dialog
  Then the lead's stage is unchanged and no conversion date is set

@story_75
Scenario: Reverting a converted lead requires extra confirmation
  Given a lead has been marked as converted
  When the user changes its stage to "Contacted"
  Then a second confirmation dialog appears before the stage change is applied
```

## Manual Tests

**Story:** [#67 — Mark Lead as Converted](../docs/047-mark-lead-as-converted.md)

### User sees the Mark as Converted button in lead details
1. Open any active (non-converted) lead
2. Confirm "Mark as Converted" button is visible

### User converts a lead and sees the confirmation dialog
1. Click "Mark as Converted"
2. Confirm a dialog appears asking for confirmation
3. Confirm and verify the lead's stage changes to "Closed"
4. Verify a success notification appears

### Conversion date is recorded correctly
1. Convert a lead and note today's date
2. Open the lead details and confirm the conversion date matches

### Converted lead is visually distinct
1. Convert a lead and return to the lead list
2. Confirm the converted lead has a green indicator or checkmark
3. Confirm active leads do not have the same indicator

### Cancelling the conversion dialog leaves the lead unchanged
1. Click "Mark as Converted" and then cancel
2. Confirm the lead's stage has not changed and no conversion date appears

### Reverting a converted lead requires extra confirmation
1. Convert a lead (stage = Closed)
2. Open it and change the stage to "Contacted"
3. Confirm a second dialog warns that the lead was previously converted
4. Confirm and verify the stage reverts; cancel and verify the stage stays "Closed"

### Mark as Converted button is not shown for already-converted leads
1. Open a converted lead
2. Confirm the "Mark as Converted" button is hidden or replaced with a "Converted" label

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/leads.feature` |
| BDD step defs | `tests/bdd/test_leads.py` |
| Unit tests | `tests/unit/leads/test_lead_conversion.py` |
| Manual tests | `tests/manual/leads/mark_converted.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
