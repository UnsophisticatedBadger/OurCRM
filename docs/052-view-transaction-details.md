# US-052 — View Transaction Details

**Capability:** Transactions
**Status:** Not Done

## User Story

As a real estate agent, I want to open a transaction and see all its information in one place, so that I can review the deal, check dates, and navigate directly to the linked property and contact records.

## Dependencies

- US-051 — View Transaction List

## Acceptance Criteria

1. Double-clicking a transaction in the list opens its details view showing all fields; optional fields with no data show "Not provided"
2. The linked property, buyer contact, and seller contact are shown as clickable links that open their respective details views
3. If both sale price and commission percentage are recorded, the commission breakdown is shown (e.g., "$500,000 × 3% = $15,000")
4. The details view has Edit and Delete buttons, a Back to List button; pressing Escape also returns to the list
5. Previous / Next buttons navigate between transactions in the current list order

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/transactions.feature`.

```gherkin
@us049
Scenario: User double-clicks a transaction and sees all its details
  Given a transaction exists with all fields filled
  When the user double-clicks it in the transaction list
  Then the details view opens showing all of the transaction's data

@us049
Scenario: User clicks the linked property and opens its details
  Given a transaction is linked to property "123 Oak St"
  When the user opens the transaction details and clicks "123 Oak St"
  Then the property details view opens for "123 Oak St"

@us049
Scenario: Commission breakdown is shown when price and percentage are recorded
  Given a transaction has sale price 500000 and commission 3%
  When the user opens the transaction details
  Then "$500,000 × 3% = $15,000" is shown

@us049
Scenario: User presses Escape and returns to the transaction list
  Given the user is viewing a transaction's details
  When the user presses Escape
  Then the transaction list is shown
```

## Manual Tests

**Story:** [US-052 — View Transaction Details](../docs/055-view-transaction-details.md)

### User opens transaction details from the list
1. Double-click a transaction in the list
2. Confirm the details view opens with all data shown
3. Confirm optional empty fields show "Not provided" rather than blank

### Linked records are clickable
1. Open a transaction linked to a property and two contacts
2. Click the property name — confirm the property details view opens
3. Navigate back, click the buyer name — confirm the contact details view opens
4. Repeat for the seller name

### Commission breakdown is displayed
1. Open a transaction with sale price $500,000 and commission 3%
2. Confirm "$500,000 × 3% = $15,000" appears in the details view

### Edit, Delete, and Back to List buttons are present
1. Confirm all three buttons are visible in the details view
2. Click "Back to List" and confirm you return to the transaction list
3. Open a transaction again and press Escape — confirm you return to the list

### Previous and Next navigation works
1. Create at least three transactions
2. Open the first transaction's details
3. Click Next and confirm the next transaction is shown
4. Click Previous and confirm the first transaction is shown again

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/transactions.feature` |
| BDD step defs | `tests/bdd/test_transactions.py` |
| Unit tests | `tests/unit/transactions/test_transaction_details.py` |
| Manual tests | `tests/manual/transactions/transaction_details.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
