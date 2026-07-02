# 33 - Currency Format By Locale

**Capability:** shell
**Milestone:** Secure Shell
**Status:** Not Done
**GitHub Issue:** #33
**Priority:** Post-MVP

## User Story
As an agent, I want monetary values to be formatted according to my locale, so that prices and amounts are immediately readable without mental conversion.

## Dependencies
- #171 — Additional Language Support

## Acceptance Criteria
1. All monetary values throughout the app (budgets, property prices, transaction amounts) are formatted using the currency convention for the locale selected in #171
2. The formatting covers symbol position, decimal separator, and thousands separator (e.g. US: $1,000.00; Spain: 1.000,00 €)
3. Settings → General → Currency allows the user to override the locale-derived currency with an explicit choice (USD, EUR, GBP, CAD, AUD); symbol and separators update to match
4. The override applies to all monetary display in the app; data is stored in the original numeric form
5. The currency setting persists across app restarts

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/shell.feature`.

```gherkin
@story_33
Scenario: Currency format follows US locale
  Given the locale is set to English (US)
  When the user views a lead's budget of 1000000
  Then it is displayed as "$1,000,000.00"

@story_33
Scenario: Currency format follows Spanish locale
  Given the locale is set to Español (Spain)
  When the user views a lead's budget of 1000000
  Then it is displayed as "1.000.000,00 €"

@story_33
Scenario: User overrides locale currency to GBP and all monetary values update
  Given the locale is English (US) but the user selects GBP as the currency override
  When the user views any monetary value
  Then it is formatted as "£1,000.00"

@story_33
Scenario: Currency format persists after app restart
  Given GBP is set as the currency override
  When the user restarts the app
  Then monetary values are still displayed in GBP format
```

## Manual Tests
**Story:** [#172 — Currency Format by Locale](../docs/141-currency-format-by-locale.md)

### Monetary values use the US locale format
1. Set the locale to English (US)
2. View a lead's budget field
3. Verify it displays as $1,000.00 (dollar sign prefix, comma thousands, period decimal)

### Monetary values use the Spanish locale format
1. Set the locale to Español (Spain)
2. View a lead's budget field
3. Verify it displays using European separators and the € symbol

### User overrides currency independently of locale
1. Go to Settings → General → Currency and select GBP
2. View a property price
3. Verify the price is formatted with the £ symbol and correct separators

### Currency format persists after restart
1. Set a currency override and restart the app
2. Verify the same currency format is still in use

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_currency_format.py` |
| Manual tests | `tests/manual/shell/currency-format.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
