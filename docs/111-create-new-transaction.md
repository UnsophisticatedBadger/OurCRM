# 111 - Create A New Transaction

**Capability:** Transactions
**Milestone:** Extended CRM
**Status:** Not Done
**GitHub Issue:** #111

## User Story

As a real estate agent, I want to create a transaction to track a deal from contract to closing, so that I can manage all parties, dates, and amounts in one place.

## Dependencies

- #6 — Log In and Out (session factory registered in DI)
- #10 — Navigate Between Sections
- #56 — Create a New Contact (contact model used for buyer/seller linking)
- #60 — Delete A Contact (contact deletion must respect the transaction link introduced by this story)
- #104 — Create a New Property Listing (property model used for property linking)

## Acceptance Criteria

1. "New Transaction" button in the Transactions section opens a form with: transaction type (Sale / Lease), property (searchable from existing properties, optional), buyer contact (searchable from existing contacts, optional), seller contact (searchable from existing contacts, optional), contract date (required), closing date (optional), sale price (optional), commission percentage (optional), status (Under Contract / Pending / Closed / Cancelled — defaults to Under Contract), and notes (optional)
2. Contract date is required; saving without it shows an inline error and keeps the form open
3. If closing date is provided, it must be on or after the contract date; saving with an earlier closing date shows "Closing date must be on or after contract date"
4. If both sale price and commission percentage are entered, the calculated commission amount is shown inline (e.g., "$500,000 × 3% = $15,000")
5. Saving a valid transaction creates it, returns to the transaction list, and the new transaction appears in it
6. Cancel closes the form without saving
7. Transactions persist across application restarts
8. A contact linked to this transaction as buyer or seller cannot be deleted while the link exists (extends #60 — Delete A Contact with a transaction-tie check, implemented via a DI-injected guard interface so the Contacts capability does not import from Transactions)

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/transactions.feature`.

```gherkin
@story_111
Scenario: User creates a transaction and sees it in the transaction list
  Given the user is in the Transactions section
  When the user clicks "New Transaction", enters contract date today and type "Sale", and clicks Save
  Then the transaction list shows the new transaction with type "Sale"

@story_111
Scenario: User submits the form with no contract date and sees an error
  Given the new transaction form is open
  When the user leaves the contract date empty and clicks Save
  Then an inline error is shown and the form stays open

@story_111
Scenario: User enters a closing date before the contract date and sees an error
  Given the new transaction form is open
  When the user enters contract date 2026-07-01 and closing date 2026-06-01 and clicks Save
  Then "Closing date must be on or after contract date" is shown

@story_111
Scenario: Commission amount is shown when price and percentage are both entered
  Given the new transaction form is open
  When the user enters sale price 500000 and commission 3
  Then the form shows "$500,000 × 3% = $15,000"

@story_111
Scenario: Transaction persists after an application restart
  Given the user has created a transaction with contract date today
  When the application is restarted and the user opens the Transactions section
  Then the transaction appears in the list
```

## Manual Tests

**Story:** [#111 — Create a New Transaction](111-create-new-transaction.md)
### User opens the new transaction form and sees all fields
1. Navigate to the Transactions section and click "New Transaction"
2. Confirm the form shows: type, property, buyer, seller, contract date, closing date, sale price, commission %, status, and notes

### User creates a transaction with all fields filled
1. Fill in all fields with valid data, link a property and two contacts, and click Save
2. Confirm the transaction list appears and the new transaction is visible
3. Open the transaction to confirm all data and links were saved correctly

### Required field validation
1. Leave contract date empty and click Save — confirm an error appears

### Date validation
1. Enter a closing date one day before the contract date
2. Confirm "Closing date must be on or after contract date" appears
3. Correct the date and confirm the transaction saves

### Commission shown inline
1. Enter sale price $500,000 and commission 3%
2. Confirm the form shows "$500,000 × 3% = $15,000"

### Contact and property linking
1. Select an existing property in the property field
2. Select existing contacts for buyer and seller
3. Save and open the transaction — confirm all three links are shown

### Transaction persists after a restart
1. Create a transaction, close the application, and restart
2. Navigate to Transactions and confirm the transaction is still there with all data intact

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/transactions.feature` |
| BDD step defs | `tests/bdd/test_transactions.py` |
| Unit tests | `tests/unit/transactions/test_transaction_form.py`, `test_transaction_repository.py` |
| Manual tests | `tests/manual/transactions/create_transaction.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
