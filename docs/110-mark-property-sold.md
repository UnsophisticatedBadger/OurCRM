# 110 - Mark Property As Sold

**Capability:** Properties
**Milestone:** Extended CRM
**Status:** Not Done
**GitHub Issue:** #110

## User Story

As a real estate agent, I want to mark a property as sold and record the sale details, so that I can track the final sale price, closing date, and buyer for each listing I close.

## Dependencies

- #106 — View Property Details
- #56 — Create a New Contact (contact model used for buyer linking)

## Acceptance Criteria

1. The property details view shows a "Mark as Sold" button for any property not already in Sold status
2. Clicking it opens a sale details form with: sale price (required), closing date (required), buyer contact (optional — searchable from existing contacts), commission percentage (optional), and notes (optional)
3. If both sale price and commission percentage are entered, the calculated commission amount is shown inline (e.g., "$500,000 × 3% = $15,000")
4. Confirming the sale sets the property status to Sold, records the sale details, and shows a brief success notification
5. The recorded sale price, closing date, buyer name, and commission details are visible in the property details view after the sale
6. Changing a sold property's status to any other value via the edit form or list right-click requires a second explicit confirmation

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/properties.feature`.

```gherkin
@story_110
Scenario: User marks a property as sold and it moves to Sold status
  Given the user is viewing an Active property
  When the user clicks "Mark as Sold", enters sale price 500000 and closing date, and confirms
  Then the property status is "Sold"
  And a success notification is shown

@story_110
Scenario: Sale details are visible in property details after the sale
  Given the user marks a property as sold with price 480000 and buyer "Jane Smith"
  When the user views the property details
  Then sale price "$480,000" and buyer "Jane Smith" are shown

@story_110
Scenario: Commission amount is calculated from sale price and percentage
  Given the sale details form is open with price 500000
  When the user enters commission percentage 3
  Then the form shows "$500,000 × 3% = $15,000"

@story_110
Scenario: User cancels the sale dialog and the property status is unchanged
  Given the user is viewing an Active property
  When the user clicks "Mark as Sold" then cancels the dialog
  Then the property status is still "Active"

@story_110
Scenario: Reverting a sold property's status requires extra confirmation
  Given a property has been marked as sold
  When the user changes its status to "Active"
  Then a second confirmation dialog appears before the status change is applied
```

## Manual Tests

**Story:** [#110 — Mark Property as Sold](110-mark-property-sold.md)
### Mark as Sold button is visible on active properties
1. Open any Active or Pending property's details
2. Confirm "Mark as Sold" button is visible

### User fills in sale details and confirms
1. Click "Mark as Sold"
2. Confirm the sale details form opens with sale price, closing date, buyer, commission %, and notes fields
3. Enter a sale price and closing date, then confirm
4. Confirm the property status changes to "Sold" and a success notification appears

### Sale details are shown in the property details view
1. Mark a property as sold with price $480,000, closing date, and buyer "Jane Smith"
2. View the property details
3. Confirm sale price, closing date, buyer name, and commission (if entered) are all visible

### Commission calculation shown inline
1. In the sale details form, enter sale price $500,000 and commission 3%
2. Confirm "$500,000 × 3% = $15,000" appears as a calculated field

### Cancelling leaves the property unchanged
1. Click "Mark as Sold" and then cancel the dialog
2. Confirm the property status has not changed

### Mark as Sold button is hidden on already-sold properties
1. Open a property already in Sold status
2. Confirm "Mark as Sold" button is not shown

### Reverting a sold property requires extra confirmation
1. Open a sold property and change its status via the edit form
2. Confirm a second dialog warns about reverting a sold property
3. Cancel — confirm the status stays Sold
4. Confirm — verify the status changes

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/properties.feature` |
| BDD step defs | `tests/bdd/test_properties.py` |
| Unit tests | `tests/unit/properties/test_mark_sold.py` |
| Manual tests | `tests/manual/properties/mark_sold.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
