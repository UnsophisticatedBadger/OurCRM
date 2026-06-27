# US-045 — View Property Details

**Capability:** Properties
**Status:** Not Done

## User Story

As a real estate agent, I want to open a property and see all its information in one place, so that I can review the full listing details without switching screens or scrolling through a table.

## Dependencies

- US-044 — View Property List

## Acceptance Criteria

1. Double-clicking a property in the list opens its details view showing all fields; optional fields with no data show "Not provided"
2. The details view has Edit and Delete buttons, a Back to List button; pressing Escape also returns to the list
3. Previous / Next buttons navigate between properties in the current list order
4. If a seller contact is linked, their name is shown as a clickable link that opens the contact's details view

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/properties.feature`.

```gherkin
@us042
Scenario: User double-clicks a property and sees all its details
  Given a property "123 Oak St" exists with all fields filled
  When the user double-clicks "123 Oak St" in the property list
  Then the details view opens showing all of the property's data

@us042
Scenario: Empty optional fields show Not provided
  Given a property "123 Oak St" exists with no MLS number or description
  When the user opens its details
  Then the MLS number and description fields show "Not provided"

@us042
Scenario: User presses Escape and returns to the property list
  Given the user is viewing a property's details
  When the user presses Escape
  Then the property list is shown

@us042
Scenario: User clicks the seller contact link and opens the contact details
  Given property "123 Oak St" has seller "Jane Smith" linked
  When the user opens the property details and clicks "Jane Smith"
  Then the contact details view opens for "Jane Smith"
```

## Manual Tests

**Story:** [US-045 — View Property Details](../docs/045-view-property-details.md)

### User opens property details from the list
1. Double-click a property in the list
2. Confirm the details view opens with all data shown
3. Confirm optional empty fields show "Not provided" rather than blank

### Edit, Delete, and Back to List buttons are present
1. Confirm all three buttons are visible in the details view
2. Click "Back to List" and confirm you return to the list
3. Open a property again and press Escape — confirm you return to the list

### Previous and Next navigation works
1. Create at least three properties
2. Open the first property's details
3. Click Next and confirm the next property is shown
4. Click Previous and confirm the first property is shown again
5. Confirm navigation wraps or disables at the ends of the list

### Seller contact link opens the contact details
1. Create a contact and link them as seller on a property
2. Open the property details and click the seller's name
3. Confirm the contact details view opens for that person
4. Navigate back to confirm you return to the property

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/properties.feature` |
| BDD step defs | `tests/bdd/test_properties.py` |
| Unit tests | `tests/unit/properties/test_property_details.py` |
| Manual tests | `tests/manual/properties/property_details.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
