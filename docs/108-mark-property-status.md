# US-059 — Change Property Status from the List

**Capability:** Properties
**Status:** Not Done
**GitHub Issue:** #108

## User Story

As a real estate agent, I want to change a property's status directly from the property list, so that I can update Active / Pending / Withdrawn without opening the full edit form.

## Dependencies

- #18 — View Property List

## Acceptance Criteria

1. Right-clicking a property in the list and selecting "Change Status" opens a small status picker with options Active, Pending, Sold, and Withdrawn
2. Selecting a new status updates the row's color indicator immediately without navigating away
3. The new status is reflected in the property details when the property is subsequently opened
4. Status changes persist across application restarts

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/properties.feature`.

```gherkin
@us044
Scenario: User right-clicks a property and changes its status from the list
  Given a property "123 Oak St" with status "Active" is in the list
  When the user right-clicks "123 Oak St" and selects "Change Status" then "Pending"
  Then the "123 Oak St" row shows status "Pending" immediately

@us044
Scenario: Status change updates the row color immediately
  Given a property with status "Active" (green) is in the list
  When the user changes its status to "Withdrawn" via right-click
  Then the row indicator changes to red immediately

@us044
Scenario: Status change persists after an application restart
  Given the user has changed a property's status to "Pending" from the list
  When the application is restarted and the user opens the Properties section
  Then the property still shows status "Pending"
```

## Manual Tests

**Story:** [US-047 — Change Property Status from the List](../docs/047-mark-property-status.md)

### User changes status via right-click without opening the edit form
1. Right-click a property in the list and select "Change Status"
2. Confirm a small status picker appears (Active / Pending / Sold / Withdrawn)
3. Select a new status and confirm the row updates immediately without navigating away

### Row color updates immediately
1. Change an Active (green) property's status to Withdrawn
2. Confirm the row indicator changes to red without a page reload

### Status change is reflected in property details
1. Change a property's status from the list
2. Open the property details
3. Confirm the details view shows the new status

### Status change persists after a restart
1. Change a property's status from the list to "Pending"
2. Close the application and restart
3. Open the Properties section and confirm the status is still "Pending"

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/properties.feature` |
| BDD step defs | `tests/bdd/test_properties.py` |
| Unit tests | `tests/unit/properties/test_property_status.py` |
| Manual tests | `tests/manual/properties/property_status.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
