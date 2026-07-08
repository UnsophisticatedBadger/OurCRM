# 37 - Record Prices In Multiple Currencies

**Capability:** shell
**Milestone:** Secure Shell
**Status:** Not Done
**GitHub Issue:** #37
**Priority:** Post-MVP

## User Story
As an agent, I want to record prices and budgets in different currencies on individual records, so that I can accurately represent international clients and foreign-currency properties.

## Dependencies
- #172 — Currency Format by Locale

## Acceptance Criteria
1. Budget fields on leads and price fields on properties and transactions include a currency selector (USD, EUR, GBP, CAD, AUD) alongside the numeric input; USD is the default
2. Each record stores the currency together with the numeric value
3. The currency and amount are displayed together wherever the field appears (e.g. "£450,000" or "€320,000"), formatted per #172 conventions for that currency
4. The currency selector on a record can be changed at any time; only the display currency changes — the stored numeric value is not converted
5. List views and filters that show or compare monetary values display each record's own currency symbol

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/shell.feature`.

```gherkin
@story_37
Scenario: User records a lead budget in EUR and it is displayed with the euro symbol
  Given the user creates a lead and selects EUR as the budget currency
  When the user enters 350000 as the budget
  Then the lead's budget is displayed as "€350,000.00"

@story_37
Scenario: Two leads with different currencies each display their own symbol in the list view
  Given one lead has a budget of $500,000 USD and another has £400,000 GBP
  When the user views the Leads list
  Then each lead shows its own currency symbol and amount

@story_37
Scenario: Changing the currency on a record updates the symbol without altering the stored number
  Given a property is recorded at 500000 USD
  When the user changes the currency to EUR
  Then the property displays "€500,000.00"
  And the stored numeric value remains 500000
```

## Manual Tests
**Story:** [#94 — Record Prices in Multiple Currencies](../docs/145-record-prices-in-multiple-currencies.md)

### Budget recorded in EUR displays the euro symbol
1. Create a new lead, select EUR from the currency selector, and enter 350000
2. Save the lead and verify the budget shows "€350,000.00" in the lead detail

### Two leads with different currencies both display correctly in the list
1. Create one lead with USD budget and another with GBP budget
2. View the Leads list and verify each shows its own currency symbol

### Changing currency updates the symbol without converting the value
1. Open a property with a USD price, change the currency to EUR, and save
2. Verify the stored numeric value is unchanged and the display now shows the € symbol

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_multi_currency.py` |
| Manual tests | `tests/manual/shell/record-prices-in-multiple-currencies.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
