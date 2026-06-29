# 107 - Edit A Property

**Capability:** Properties
**Milestone:** v0.8.0 — Extended CRM
**Status:** Not Done
**GitHub Issue:** #107

## User Story

As a real estate agent, I want to edit a property's information at any time, so that I can keep price, status, description, and other details current as the listing evolves.

## Dependencies

- #19 — View Property Details

## Acceptance Criteria

1. The Edit button on the property details view opens an edit form pre-populated with all of the property's current data
2. All fields can be changed; validation rules match the create form (address and price required; price must be positive)
3. Saving updates the property, returns to the details view with the new values shown immediately, and reflects the changes in the property list row
4. A property can also be opened for editing from the list via right-click > Edit or Ctrl+E
5. Cancel discards all changes and returns to the details view with the original data unchanged
6. All edits persist across application restarts

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/properties.feature`.

```gherkin
@story_17
Scenario: User opens the edit form and sees all fields pre-populated
  Given the user is viewing a property with listing price 450000
  When the user clicks Edit
  Then the edit form opens with the price field showing 450000

@story_17
Scenario: User edits the listing price and sees it updated in details and list
  Given the user is editing a property with price 450000
  When the user changes the price to 425000 and clicks Save
  Then the details view shows "$425,000"
  And the property list row also shows "$425,000"

@story_17
Scenario: Saving with the address cleared shows a validation error
  Given the user is editing a property
  When the user clears the street address and clicks Save
  Then an inline error is shown and the form stays open

@story_17
Scenario: User cancels an edit and the original data is unchanged
  Given the user is editing a property with price 450000
  When the user changes the price to 300000 and clicks Cancel
  Then the details view still shows "$450,000"
```

## Manual Tests

**Story:** [#70 — Edit a Property](../docs/046-edit-propety.md)

### User opens the edit form and sees all fields pre-populated
1. Open any property's details and click Edit
2. Confirm every field is pre-populated with the property's current data
3. Confirm the form title distinguishes editing from creating

### User edits the listing price and sees it in details and list
1. Change the listing price to a new value and save
2. Confirm the details view shows the new price immediately
3. Navigate back to the list and confirm the row shows the new price

### Validation rejects a cleared address
1. Clear the street address and click Save
2. Confirm an inline error appears and the form stays open
3. Restore the address and confirm the property saves

### Price validation still applies in the edit form
1. Enter a negative price and click Save
2. Confirm "Listing price must be greater than zero" appears

### Cancel discards changes
1. Open the edit form and change several fields
2. Click Cancel
3. Confirm the details view shows the original data

### Edit from the list via right-click
1. Right-click a property in the list and select "Edit"
2. Confirm the edit form opens pre-populated
3. Test Ctrl+E and confirm it also opens the edit form

### All edits persist after a restart
1. Edit a property's price and description, then save
2. Close the application and restart
3. Open the property and confirm all changes are still shown

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/properties.feature` |
| BDD step defs | `tests/bdd/test_properties.py` |
| Unit tests | `tests/unit/properties/test_property_editing.py` |
| Manual tests | `tests/manual/properties/edit_property.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
