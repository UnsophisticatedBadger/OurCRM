# US-122 — View Qualification History

**Capability:** AI Features
**Status:** Not Done

## User Story

As a real estate agent, I want to view the full history of a lead's AI qualifications and manual overrides, so that I can see how the assessment has evolved over time.

## Dependencies

- US-090 — Qualify a Lead with AI
- US-092 — Override AI Qualification

## Acceptance Criteria

1. A qualification history section is accessible on a lead's detail view
2. The history lists all qualification events in reverse chronological order (newest first)
3. Each AI qualification event shows: timestamp, score, and status
4. Each manual override event shows: timestamp, agent-chosen status, and any override notes
5. When no qualification events have been recorded for a lead, the section shows "No qualification history yet"

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/ai.feature`.

```gherkin
@us068
Scenario: History shows AI qualification and manual override in reverse chronological order
  Given a lead was AI-qualified with score 30 and status "Cold" at 10:00 AM
  And the agent overrode it to status "Hot" with note "Very motivated" at 11:00 AM
  When the user views the qualification history
  Then the 11:00 AM override event appears first, showing status "Hot" and note "Very motivated"
  And the 10:00 AM AI event appears below it, showing score 30 and status "Cold"

@us068
Scenario: Re-qualification adds a new event without removing older events
  Given a lead was qualified at 9:00 AM with score 40
  When the user re-qualifies the lead at 2:00 PM and the AI returns score 75
  Then the history shows the 2:00 PM event (score 75) first
  And the 9:00 AM event (score 40) is still present below it

@us068
Scenario: Lead with no history shows an appropriate message
  Given a lead has never been qualified by AI
  When the user views the qualification history section
  Then "No qualification history yet" is displayed
```

## Manual Tests

**Story:** [US-122 — View Qualification History](../docs/106-view-qualification-history.md)

### History shows all events in reverse chronological order
1. Qualify a lead, note the time and result
2. Override the qualification, note the time and chosen status
3. Re-qualify the lead, note the time and new result
4. Open the qualification history
5. Confirm three events are listed with the most recent at the top
6. Confirm each event shows its timestamp and the relevant details (score/status for AI events; status + notes for overrides)

### History does not lose older events after re-qualification
1. Qualify a lead to create an initial event
2. Re-qualify the lead
3. Confirm the history shows both events — the new one at the top and the original below

### Empty history state
1. Create a new lead and do not qualify it
2. Open the qualification history section
3. Confirm "No qualification history yet" is displayed

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/ai.feature` |
| BDD step defs | `tests/bdd/test_ai.py` |
| Unit tests | `tests/unit/ai/test_qualification_history.py` |
| Manual tests | `tests/manual/ai/qualification_history.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
