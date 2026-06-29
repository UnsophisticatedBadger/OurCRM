# US-048 — Edit a Lead

**Capability:** Leads
**Status:** Not Done

## User Story

As a real estate agent, I want to edit a lead's information at any time, so that I can keep their status, budget, source, and other details up to date as their situation changes.

## Dependencies

- US-035 — View Lead List

## Acceptance Criteria

1. The Edit button on the lead details view opens an edit form pre-populated with all of the lead's current data
2. All fields can be changed; validation rules match the create form (US-034) — name and status are required; if both budget fields are filled, min must not exceed max
3. The source dropdown has the same predefined options as the create form; selecting "Other" shows a free-text field for a custom source
4. Saving updates the lead, returns to the details view with the new values shown immediately, and reflects the changes in the lead list row
5. Lead status can also be changed directly from the lead list via right-click > Change Status without opening the full edit form
6. Cancel discards all changes and returns to the details view with the original data unchanged
7. All edits persist across application restarts

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/leads.feature`.

```gherkin
@us032
Scenario: User edits a lead's status and sees the update in list and details
  Given the user is viewing a lead with status "Warm"
  When the user clicks Edit, changes the status to "Hot", and clicks Save
  Then the details view shows status "Hot"
  And the lead list row also shows "Hot"

@us032
Scenario: User edits a lead's budget and sees the formatted range
  Given the user is editing a lead
  When the user sets min budget to 300000 and max budget to 500000 and saves
  Then the details view shows "$300,000 – $500,000"

@us032
Scenario: Saving with min budget greater than max shows an error
  Given the user is editing a lead's budget
  When the user enters min 500000 and max 300000 and clicks Save
  Then "Minimum budget cannot be greater than maximum budget" is shown and the form stays open

@us032
Scenario: User selects Other as source and enters a custom value
  Given the user is editing a lead
  When the user selects "Other" from the source dropdown, types "Real Estate Expo", and saves
  Then the details view shows source "Real Estate Expo"

@us032
Scenario: User cancels an edit and the original data is unchanged
  Given the user is editing a lead with status "Cold"
  When the user changes the status to "Hot" and clicks Cancel
  Then the details view still shows status "Cold"

@us032
Scenario: User changes status directly from the lead list
  Given the user is viewing the lead list
  When the user right-clicks a lead and selects "Change Status" then "Cold"
  Then the lead's status in the list updates to "Cold" immediately

@us032
Scenario: All edits persist after an application restart
  Given the user has set a lead's status to "Hot" and budget to 400000–600000
  When the application is restarted and the user opens that lead
  Then the status is "Hot" and the budget shows "$400,000 – $600,000"
```

## Manual Tests

**Story:** [US-036 — Edit a Lead](../docs/038-assign-lead-status.md)

### User opens the edit form and sees all fields pre-populated
1. Open any lead's details and click Edit
2. Confirm every field is pre-populated with the lead's current data
3. Confirm the form title distinguishes editing from creating

### User edits status and sees it reflected in details and list
1. Change the status to "Hot" and save
2. Confirm the details view shows "Hot" with the red indicator
3. Navigate back to the list and confirm the row also shows "Hot"

### Budget validation rejects min > max
1. Enter min $600,000 and max $400,000, click Save
2. Confirm "Minimum budget cannot be greater than maximum budget" appears
3. Fix the values and confirm the lead saves

### Budget range is displayed formatted after editing
1. Set budget min $300,000 and max $500,000 and save
2. Confirm the details and list both show "$300,000 – $500,000"

### Custom source via "Other"
1. Select "Other" from the source dropdown
2. Confirm a free-text field appears
3. Enter "Neighbourhood flyer" and save
4. Confirm the lead shows "Neighbourhood flyer" as the source

### Cancel discards changes
1. Open the edit form and change several fields
2. Click Cancel
3. Confirm the details view still shows the original data

### Status can be changed from the list without opening the edit form
1. Right-click a lead in the list and choose "Change Status"
2. Select a new status
3. Confirm the row updates immediately without navigating away

### All edits survive a restart
1. Edit a lead's status, budget, and source, then save
2. Close the application and restart
3. Open the lead and confirm all changes are still shown

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/leads.feature` |
| BDD step defs | `tests/bdd/test_leads.py` |
| Unit tests | `tests/unit/leads/test_lead_editing.py` |
| Manual tests | `tests/manual/leads/edit_lead.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
