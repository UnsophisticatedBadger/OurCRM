# 104 - Create A New Property Listing

**Capability:** Properties
**Milestone:** Extended CRM
**Status:** Not Done
**GitHub Issue:** #104

## User Story

As a real estate agent, I want to create a new property listing with its details, so that I can track the properties I represent alongside the contacts and leads in the same CRM.

## Dependencies

- #6 — Log In and Out (session factory registered in DI)
- #10 — Navigate Between Sections
- #43 — Create a New Contact (contact model used for seller linking)

## Acceptance Criteria

1. "New Property" button in the Properties section opens a form with fields for property type (Single Family / Condo / Townhouse / Land / Multi-Family / Commercial), street address, city, state, ZIP code, bedrooms, bathrooms, square feet, lot size, year built, listing price, status (Active / Pending / Sold / Withdrawn), MLS number (optional), and description (optional)
2. Street address and listing price are required; saving with either empty shows an inline error and keeps the form open
3. Listing price must be a positive number; saving with zero or a negative value shows "Listing price must be greater than zero"
4. An optional seller field allows searching for and selecting an existing contact; the selected contact is linked to the property as its seller
5. Saving a valid property creates it, returns to the property list, and the new property appears in it
6. Cancel closes the form without saving
7. Properties persist across application restarts

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/properties.feature`.

```gherkin
@story_104
Scenario: User creates a property and sees it in the property list
  Given the user is in the Properties section
  When the user clicks "New Property", fills in address "123 Oak St" and price 450000, and clicks Save
  Then the property list shows "123 Oak St" with listing price "$450,000"

@story_104
Scenario: User submits the form with no street address and sees an error
  Given the new property form is open
  When the user leaves the street address empty and clicks Save
  Then an inline error is shown and the form stays open

@story_104
Scenario: User enters a negative listing price and sees a validation error
  Given the new property form is open
  When the user enters listing price -100 and clicks Save
  Then "Listing price must be greater than zero" is shown

@story_104
Scenario: User links a seller contact and the link appears in property details
  Given a contact "Jane Smith" exists
  And the new property form is open
  When the user selects "Jane Smith" in the seller field and saves the property
  Then opening the property details shows "Jane Smith" as the linked seller

@story_104
Scenario: Property persists after an application restart
  Given the user has created a property "123 Oak St"
  When the application is restarted and the user opens the Properties section
  Then "123 Oak St" appears in the property list
```

## Manual Tests

**Story:** [#17 — Create a New Property Listing](../docs/043-create-property-listing.md)

### User opens the new property form and sees all fields
1. Navigate to the Properties section and click "New Property"
2. Confirm the form shows all fields: type, address, city, state, ZIP, beds, baths, sq ft, lot size, year built, price, status, MLS number, and description

### User creates a property with all fields filled
1. Fill in all fields with valid data and click Save
2. Confirm the property list appears and the new property is visible
3. Open the property to confirm all data was saved correctly

### Required field validation
1. Leave street address empty and click Save — confirm an error appears
2. Clear the listing price and click Save — confirm a price error appears

### Price validation
1. Enter a negative listing price and click Save
2. Confirm "Listing price must be greater than zero" appears
3. Enter 0 — confirm the same error appears
4. Correct the price and confirm the property saves

### Seller contact linking
1. Ensure a contact exists (create one if needed)
2. In the new property form, search for and select that contact in the seller field
3. Save the property and open its details
4. Confirm the seller's name is shown as a link

### Property persists after a restart
1. Create a property, close the application, and restart
2. Navigate to Properties and confirm the property is still there with all data intact

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/properties.feature` |
| BDD step defs | `tests/bdd/test_properties.py` |
| Unit tests | `tests/unit/properties/test_property_form.py`, `test_property_repository.py` |
| Manual tests | `tests/manual/properties/create_property.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
