# 183 - View AI Qualification Results

**Capability:** AI Features
**Milestone:** Post-Production
**Status:** Not Done
**GitHub Issue:** #183

## User Story

As a real estate agent, I want the AI qualification result to be displayed clearly on a lead's detail view and summarised in the lead list, so that I can understand the AI's assessment at a glance and identify my hottest leads quickly.

## Dependencies

- #136 — Qualify a Lead with AI

## Notes

This story specifies the display format of qualification results. The AI call and storage are owned by #136; this story owns the visual presentation: colour coding, score rendering, lead-list badge, and the unqualified state.

**Third-party testability:** All scenarios here operate on *already-stored* qualification data and do not call a live AI provider. BDD and unit tests can seed a qualification result directly via the repository layer without going through the AI service. No `@live_ai` tagging is needed for this story.

## Acceptance Criteria

1. The qualification panel on a lead's detail view shows the score as both a number and a colour-coded bar: green for high scores, yellow for mid-range, red for low scores
2. The qualification status is colour-coded: Hot = red, Warm = orange, Cold = blue
3. The reasoning is displayed as readable paragraphs, not raw JSON or code
4. A lead that has never been qualified shows "Not yet qualified" in the qualification panel with a "Qualify with AI" button
5. A lead that has been qualified shows a "Re-qualify" button in the qualification panel
6. The lead list shows an AI status badge (Hot / Warm / Cold) next to each lead that has been qualified; unqualified leads show a dash

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/ai.feature`.

```gherkin
@story_183
Scenario: Qualified lead shows colour-coded score, status, reasoning, and date
  Given a lead has been qualified with score 78 and status "Hot"
  When the user views the lead's detail view
  Then the qualification panel shows "78" as the score with a colour-coded bar
  And the status "Hot" is displayed in red
  And the reasoning is displayed as readable text
  And the qualification date is shown

@story_183
Scenario: Unqualified lead shows "Not yet qualified" and a prompt
  Given a lead has never been qualified by AI
  When the user views the lead's detail view
  Then the qualification panel shows "Not yet qualified"
  And a "Qualify with AI" button is present in the panel

@story_183
Scenario: Qualified lead shows a Re-qualify button
  Given a lead has already been qualified by AI
  When the user views the lead's detail view
  Then a "Re-qualify" button is present in the qualification panel

@story_183
Scenario: Lead list shows AI status badges for qualified leads
  Given lead "Alice Smith" is qualified as "Hot" and lead "Bob Jones" is qualified as "Cold"
  And lead "Carol White" has not been qualified
  When the user views the lead list
  Then "Alice Smith" shows a "Hot" badge
  And "Bob Jones" shows a "Cold" badge
  And "Carol White" shows a dash or "—" in the AI status column
```

## Manual Tests

**Story:** [#22 — View AI Qualification Results](../docs/023-view-ai-qualification-results.md)

### Qualification panel shows score, colour-coded status, reasoning, and date
1. Qualify a lead and view its detail page
2. Confirm the score is shown as a number with a colour-coded bar next to it
3. Confirm the status (Hot / Warm / Cold) is colour-coded: Hot = red, Warm = orange, Cold = blue
4. Confirm the reasoning is shown as readable text — not raw code or JSON
5. Confirm the qualification date and time are shown

### Unqualified lead shows the right empty state
1. Create a new lead and do not qualify it
2. Open its detail view and look at the qualification panel
3. Confirm it reads "Not yet qualified" and shows a "Qualify with AI" button

### Qualified lead shows Re-qualify button
1. Open any qualified lead's detail view
2. Confirm a "Re-qualify" button is visible in the qualification panel
3. Confirm the button triggers a new AI call (covered in #136 tests)

### Lead list shows AI status badges
1. Qualify several leads with different statuses
2. Leave at least one lead unqualified
3. View the lead list
4. Confirm each qualified lead shows its Hot / Warm / Cold badge
5. Confirm unqualified leads show a dash in the AI status column
6. Confirm the badges match the statuses seen in each lead's detail view

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/ai.feature` |
| BDD step defs | `tests/bdd/test_ai.py` |
| Unit tests | `tests/unit/ai/test_qualification_display.py` |
| Manual tests | `tests/manual/ai/qualification_display.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
