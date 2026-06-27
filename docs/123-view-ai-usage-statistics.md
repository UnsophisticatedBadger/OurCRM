# US-123 — View AI Usage Statistics

**Capability:** AI Features
**Status:** Not Done

## User Story

As a real estate agent, I want to see how many leads I have qualified with AI and how often I override it, so that I can understand the value I am getting from the AI feature.

## Dependencies

- US-090 — Qualify a Lead with AI
- US-089 — Configure AI Settings

## Acceptance Criteria

1. An AI Usage statistics view is accessible (e.g., from Settings → AI or a Reports area)
2. The view shows: total leads qualified all-time, leads qualified in the selected period, total manual overrides in the selected period, and override rate as a percentage
3. The currently configured AI provider name is shown
4. A time period selector (This Month / This Quarter / This Year / All Time) filters the period-based metrics while keeping the all-time total unchanged
5. When no AI qualifications have been run, the view shows "No AI usage yet"

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/ai.feature`.

```gherkin
@us069
Scenario: Statistics show correct totals after qualifying leads
  Given the agent has qualified 5 leads and manually overridden 2 of them
  When the user opens AI Usage statistics
  Then "Total leads qualified" shows "5"
  And "Manual overrides" shows "2"
  And "Override rate" shows "40%"

@us069
Scenario: Time period selector filters the period metrics
  Given 3 leads were qualified this month and 4 were qualified last month (7 total)
  When the user selects "This Month" from the time period selector
  Then "Leads qualified this period" shows "3"
  And "Total leads qualified (all time)" still shows "7"

@us069
Scenario: No usage yet shows appropriate empty state
  Given no leads have been qualified with AI
  When the user opens AI Usage statistics
  Then "No AI usage yet" is displayed
```

## Manual Tests

**Story:** [US-123 — View AI Usage Statistics](../docs/107-view-ai-usage-statistics.md)

### Statistics show accurate counts
1. Qualify five leads using AI
2. Manually override two of them
3. Open AI Usage statistics
4. Confirm total leads qualified = 5, overrides = 2, override rate = 40%
5. Confirm the currently configured provider name is shown

### Time period selector updates the period metrics only
1. Qualify leads over multiple months
2. Open AI Usage statistics
3. Select "This Month" and confirm only this month's qualifications and overrides are counted
4. Select "All Time" and confirm all qualifications are counted
5. Confirm the all-time total does not change when the period selector changes

### Empty state when no AI has been used
1. Ensure no leads have been qualified (or use a fresh database)
2. Open AI Usage statistics
3. Confirm "No AI usage yet" is shown instead of zeros

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/ai.feature` |
| BDD step defs | `tests/bdd/test_ai.py` |
| Unit tests | `tests/unit/ai/test_ai_usage_statistics.py` |
| Manual tests | `tests/manual/ai/ai_usage_statistics.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
