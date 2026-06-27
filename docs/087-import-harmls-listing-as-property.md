# US-087 — Import HAR Listing as Property

**Capability:** MLS Integration
**Status:** Not Done

## User Story

As a real estate agent, I want to import a HAR listing into my Properties so that I can track it, schedule showings for it, and link it to interested buyers without manually re-entering the data.

## Dependencies

- US-085 — Fetch HAR MLS Listings
- US-043 — Create a New Property Listing

## Notes

Import is available from two entry points: the listing row in the fetched/searched listings view and the listing detail view (US-088). Both trigger the same operation.

The MLS number is stored on the imported property record as a non-editable reference field so the source can always be traced. All other fields are editable after import.

## Acceptance Criteria

1. An "Import as Property" action is available on each HAR listing row and in the listing detail view (US-088)
2. Triggering it creates a property record pre-populated from HAR data: address, price, bedrooms, bathrooms, square footage, property type, and MLS number
3. The imported property is labelled "MLS Import" in the Properties list and its detail view, with the MLS number displayed as a read-only field
4. If a property with the same MLS number already exists, the user is warned and offered two options: Update the existing property with the latest HAR data, or Cancel
5. After a successful import, a confirmation shows with a "Go to Property" link that navigates to the new property record
6. The imported property is fully editable and appears in the Properties section alongside all other properties

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/mls.feature`.

```gherkin
@us103
Scenario: Importing a HAR listing creates a property with MLS data pre-filled
  Given HAR listing MLS#12345 with address "123 Oak St", price $450,000, 3 beds, 2 baths is in the listings view
  When the user clicks "Import as Property" on that listing
  Then a property record is created with address "123 Oak St", price $450,000, 3 beds, 2 baths, and MLS number 12345
  And the property appears in the Properties section labelled "MLS Import"

@us103
Scenario: Importing a duplicate MLS number warns the user
  Given a property with MLS#12345 already exists in the database
  When the user clicks "Import as Property" on a HAR listing with MLS#12345
  Then a warning is shown: "A property with MLS#12345 already exists"
  And the user is offered "Update existing" or "Cancel"

@us103
Scenario: Choosing Update overwrites the existing property with fresh HAR data
  Given the duplicate warning is shown for MLS#12345
  When the user clicks "Update existing"
  Then the existing property record is updated with the current HAR listing data

@us103
Scenario: Imported property is editable after import
  Given a property has been imported from HAR listing MLS#12345
  When the user opens the property and changes the price
  Then the new price is saved and the MLS number reference is still shown
```

## Manual Tests

**Story:** [US-087 — Import HAR Listing as Property](../docs/087-import-harmls-listing-as-property.md)

### Import from the listing row
1. Fetch or search HAR listings
2. Click "Import as Property" on any listing row
3. Confirm a success confirmation appears with a "Go to Property" link
4. Click the link and confirm the property record shows the correct address, price, beds, baths, and MLS number
5. Confirm the property is labelled "MLS Import"

### Import from the listing detail view
1. Open a HAR listing's detail view (US-088)
2. Click "Import as Property"
3. Confirm the same result as above

### Duplicate import shows a warning
1. Import a listing (note its MLS number)
2. Attempt to import the same listing again
3. Confirm a warning appears naming the duplicate MLS number
4. Click "Update existing" and confirm the property record is refreshed
5. Click Cancel on another attempt and confirm no change is made

### Imported property is fully editable
1. Import a listing
2. Open the property and edit the price
3. Save and confirm the edit persists
4. Confirm the MLS number field is still present and read-only

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/mls.feature` |
| BDD step defs | `tests/bdd/test_mls.py` |
| Unit tests | `tests/unit/mls/test_listing_import.py` |
| Manual tests | `tests/manual/mls/listing_import.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
