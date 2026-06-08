# US-160: Currency Format by Locale

## User Story

**As an** international user  
**I want to** see currency in my local format  
**So that** I can understand prices and values without confusion

## Priority

**Future:** Post-MVP

**Rationale:** Currency formatting varies by country ($1,000.00 vs 1.000,00 €). Proper formatting prevents confusion and errors in financial data.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 2 hours: Design currency format settings
- 3 hours: Implement currency formatting
- 2 hours: Add multiple currency support
- 2 hours: Test formatting
- 2 hours: Test on all platforms

## Dependencies

**Depends on:** US-159 (Additional Language Translations)

**Blocks:** None

## Description

Currency should be formatted according to user's locale:
- Symbol position ($100 vs 100€)
- Decimal separator (1,000.00 vs 1.000,00)
- Thousands separator
- Currency symbol

Users can also override with custom currency settings.

## BDD Scenarios

### Scenario 1: Currency matches locale

Given I have set my locale to Spanish (Spain) When I view prices Then they should show as "1.000,00 €"


### Scenario 2: Currency matches locale (US)

Given I have set my locale to English (US) When I view prices Then they should show as "$1,000.00"


### Scenario 3: Override currency

Given I have a locale When I override currency settings Then my custom format should be used


### Scenario 4: All monetary values formatted

Given I am using the application When I view any monetary value Then it should be properly formatted


### Scenario 5: Currency in reports

Given I generate a report When monetary values are shown Then they should use my currency format


### Scenario 6: Multiple currencies supported

Given I work with international clients When I enter prices Then I can choose the currency (USD, EUR, GBP, etc.)


### Scenario 7: Currency conversion (future)

Given I have prices in different currencies When I view totals Then they can be converted to my base currency


### Scenario 8: Currency persists

Given I have set currency format When I restart the app Then my format should be remembered


## Manual Testing Steps

### Test 1: Test locale currency

1. Set locale
2. View prices
3. Verify format correct

### Test 2: Test US format

1. Set US locale
2. Verify $1,000.00 format

### Test 3: Test European format

1. Set European locale
2. Verify 1.000,00 € format

### Test 4: Test override

1. Override currency
2. Verify custom format used

### Test 5: Test all values

1. Check all monetary displays
2. Verify all formatted

### Test 6: Test reports

1. Generate report
2. Verify currency format

### Test 7: Test multiple currencies

1. Enter USD price
2. Enter EUR price
3. Verify both work

### Test 8: Test on all platforms

1. Test Windows, macOS, Linux
2. Verify all work

## Acceptance Criteria

- [ ] Currency format matches locale
- [ ] Symbol position correct
- [ ] Decimal separator correct
- [ ] Thousands separator correct
- [ ] Can override currency format
- [ ] All monetary values formatted
- [ ] Reports use correct format
- [ ] Multiple currencies supported
- [ ] Currency persists across restarts
- [ ] Works on Windows, macOS, and Linux