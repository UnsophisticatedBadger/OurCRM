# US-101 — Override AI Qualification

**Capability:** AI Features
**Status:** Not Done

## User Story

As a real estate agent, I want to override the AI's qualification with my own status and an explanatory note, so that my judgement takes precedence when I have context the AI does not.

## Dependencies

- US-091 — View AI Qualification Results

## Notes

The override does not delete the AI's result — it records the agent's chosen status alongside the AI's original score and reasoning. Both remain visible in the qualification panel, clearly labelled. The override is added as an event to the qualification history (US-122).

**Third-party testability:** All scenarios here operate on stored qualification data and do not invoke a live AI provider. Seed the initial AI qualification result via the repository layer in test setup rather than calling the real AI service.

## Acceptance Criteria

1. On any lead that has been AI-qualified, the qualification panel includes an "Override" action that lets the agent choose a status (Hot / Warm / Cold) and optionally add a note
2. After saving an override, the lead displays the agent-chosen status as the active status, with a "Manual override" label
3. The AI's original score and reasoning remain visible in the qualification panel, shown in a secondary "AI assessment" section
4. The override (agent status, notes, timestamp) is recorded as an event in the lead's qualification history (US-122)
5. A lead can be re-qualified by AI after an override; the new AI result becomes the active assessment and the override is recorded in history

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/ai.feature`.

```gherkin
@us067
Scenario: Agent overrides an AI qualification and the new status is shown with a manual label
  Given a lead has been AI-qualified with status "Cold"
  When the agent clicks "Override", selects status "Hot", adds note "Met personally — very motivated", and saves
  Then the lead displays status "Hot" with a "Manual override" label
  And the AI's original "Cold" assessment is still visible in the secondary "AI assessment" section

@us067
Scenario: AI original assessment remains accessible after an override
  Given a lead has been overridden to "Hot" with the AI's original score of 28
  When the user views the lead's qualification panel
  Then the AI's score "28" and its reasoning are shown in the "AI assessment" section

@us067
Scenario: Override is recorded in the qualification history
  Given a lead was AI-qualified as "Cold" at 10:00 AM
  When the agent overrides it to "Hot" at 11:00 AM with note "Very motivated buyer"
  And the user views the qualification history
  Then the 11:00 AM override event shows status "Hot" and note "Very motivated buyer"
  And the 10:00 AM AI event is also present showing status "Cold"

@us067
Scenario: Re-qualifying after an override makes the new AI result the active assessment
  Given a lead has been overridden to "Hot" by the agent
  When the agent clicks "Re-qualify" and the AI returns status "Warm"
  Then the active status shown is "Warm" (not "Manual override")
  And the override is preserved in the qualification history
```

## Manual Tests

**Story:** [US-092 — Override AI Qualification](../docs/028-override-ai-qualification.md)

### Agent overrides an AI qualification and the override is labelled clearly
1. Qualify a lead with AI and note its status (e.g., "Cold")
2. Click "Override" in the qualification panel
3. Select a different status (e.g., "Hot") and add a note explaining why
4. Save the override
5. Confirm the lead now shows status "Hot" with a "Manual override" label
6. Confirm the AI's original "Cold" assessment and score are still visible in a secondary section

### Override notes are saved and visible
1. Perform an override with a detailed note
2. Close the lead and reopen it
3. Confirm the note is still displayed in the qualification panel

### Override appears in qualification history
1. Qualify a lead, then override it
2. Open the qualification history (US-122)
3. Confirm the override event appears with the agent's chosen status and notes
4. Confirm the original AI qualification event is also present

### Re-qualifying after an override restores AI control
1. Override a lead to "Hot"
2. Click "Re-qualify"
3. Confirm the new AI result is shown as the active assessment (no "Manual override" label)
4. Confirm the override is still visible in the qualification history

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/ai.feature` |
| BDD step defs | `tests/bdd/test_ai.py` |
| Unit tests | `tests/unit/ai/test_qualification_override.py` |
| Manual tests | `tests/manual/ai/qualification_override.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
