# US-090 — Qualify a Lead with AI

**Capability:** AI Features
**Status:** Not Done

## User Story

As a real estate agent, I want to trigger AI qualification on a lead and receive a score, status, and reasoning, so that I can prioritise my follow-ups based on an objective assessment of each lead's readiness to buy.

## Dependencies

- US-089 — Configure AI Settings
- US-034 — Create a New Lead

## Notes

AI qualification sends the lead's stored data (budget, timeline, notes, current status) to the configured provider (Ollama or OpenAI) and returns a structured result. The button is only shown when a provider other than None is configured.

**Third-party testability:** The AI provider's response is non-deterministic — BDD scenarios must assert only on the *structure* of the result (score is an integer 0–100, status is one of Hot/Warm/Cold, reasoning is non-empty text), never on specific AI-generated values. Scenarios that invoke a live provider must be tagged `@live_ai` and skipped in CI; the qualification service should be covered by unit tests using a stubbed provider that returns a fixed structured response.

## Acceptance Criteria

1. A "Qualify with AI" button is visible on any lead's detail view when an AI provider is configured (i.e., not None)
2. Clicking the button submits the lead's data to the configured AI provider and shows a progress indicator during analysis
3. When analysis completes, the lead's qualification panel shows: a score (integer 0–100), a status (Hot / Warm / Cold), and the AI's reasoning as readable text
4. The qualification result (score, status, reasoning, and timestamp) is saved with the lead and persists across application restarts
5. A lead can be re-qualified at any time; the new result replaces the current displayed result and the previous result is added to qualification history (US-122)
6. If the AI provider is unreachable or returns an error, a clear error message is shown and the lead's existing qualification is unchanged
7. When the AI provider is set to None, the "Qualify with AI" button is not shown on any lead

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/ai.feature`.

```gherkin
@us065
Scenario: User qualifies a lead and receives a structured result
  Given a lead "Alice Smith" exists with notes "Pre-approved, actively looking"
  And an AI provider is configured
  When the user clicks "Qualify with AI" on Alice Smith's detail view
  Then a progress indicator is shown during analysis
  And when complete, the qualification panel shows a score (0–100), a status (Hot / Warm / Cold), reasoning text, and a qualification timestamp

@us065
Scenario: Qualification result persists after the application restarts
  Given a lead has been qualified with score 78, status "Hot", and reasoning "Pre-approved buyer"
  When the user restarts the application and opens that lead's detail view
  Then the score "78", status "Hot", reasoning, and qualification timestamp are still displayed

@us065
Scenario: Re-qualifying a lead updates the result
  Given a lead has a qualification result with score 40
  And additional notes have been added to the lead
  When the user clicks "Qualify with AI" again and the AI returns score 72
  Then the displayed score is "72" and the qualification timestamp is updated

@us065
Scenario: AI provider error leaves the existing qualification unchanged
  Given a lead has a qualification score of 60
  And the AI provider is unreachable
  When the user clicks "Qualify with AI"
  Then a clear error message is shown
  And the lead's qualification score remains "60"

@us065
Scenario: Qualify with AI button is hidden when AI is disabled
  Given the AI provider is set to "None" in AI settings
  When the user opens any lead's detail view
  Then the "Qualify with AI" button is not visible
```

## Manual Tests

**Story:** [US-090 — Qualify a Lead with AI](../docs/026-qualify-a-lead-with-ai.md)

### User qualifies a lead and receives a structured result
1. Configure an AI provider in Settings → AI (Ollama or OpenAI)
2. Create a lead with complete data (budget, timeline, notes, current status)
3. Open the lead's detail view and click "Qualify with AI"
4. Confirm a progress indicator appears during analysis
5. Confirm the result shows a numeric score (0–100), a status (Hot / Warm / Cold), and reasoning text
6. Note the qualification timestamp

### Qualification result persists across restarts
1. Qualify a lead and note the score and status
2. Close and reopen the application
3. Open the same lead and confirm the score, status, reasoning, and timestamp are unchanged

### Re-qualification updates the displayed result
1. Qualify a lead and note the score
2. Add new notes to the lead to change its profile
3. Click "Qualify with AI" again
4. Confirm the result updates and the timestamp is refreshed

### Error handling when the AI provider is unavailable
1. Qualify a lead successfully and note the score
2. Disconnect from the internet (cloud provider) or stop Ollama
3. Click "Qualify with AI" on the same lead
4. Confirm a clear error message appears
5. Confirm the lead's existing qualification is unchanged
6. Restore the provider connection and confirm qualification works again

### Qualify with AI button hidden when AI is disabled
1. Open Settings → AI and set the provider to "None"
2. Open any lead's detail view
3. Confirm the "Qualify with AI" button is not visible

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/ai.feature` |
| BDD step defs | `tests/bdd/test_ai.py` |
| Unit tests | `tests/unit/ai/test_lead_qualification.py` |
| Manual tests | `tests/manual/ai/lead_qualification.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
