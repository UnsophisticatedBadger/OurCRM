# US-197 — Search with Natural Language

**Capability:** ai
**Status:** Not Done
**GitHub Issue:** #201
**Priority:** Post-MVP

## User Story
As an agent, I want to search my data using natural language, so that I can find records without knowing exact field names or filter options.

## Dependencies
- #135 — Configure AI Settings
- #58 — Search Contacts Globally

## Acceptance Criteria
1. The global search overlay (US-030) accepts natural language queries in addition to keyword search
2. The AI parses the query and translates it into structured filters applied across contacts, leads, properties, and transactions
3. Supported query patterns include: date ranges ("added last month"), status ("hot leads"), source ("from Zillow"), and activity ("emailed this week")
4. Results are grouped by entity type (Contacts, Leads, Properties, Transactions) and displayed in the search overlay
5. Ambiguous queries return the best-matching results without requiring the user to reformulate; no clarification dialog is shown
6. The user can refine a natural language query by editing it in the search field; results update on re-submit
7. A successful natural language query can be saved as a named saved search (per US-117)
8. If AI is not configured, natural language queries fall back to keyword search with no error

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/ai.feature`.

```gherkin
@us153
Scenario: Natural language date query returns records from the specified period
  Given AI is configured
  And contacts were added in the previous calendar month
  When the user types "contacts added last month" in the search overlay
  Then only contacts added in the previous calendar month are shown

@us153
Scenario: Natural language status query returns matching leads
  Given AI is configured
  And leads with "Hot" status exist
  When the user types "hot leads" in the search overlay
  Then only Hot leads are shown under the Leads section

@us153
Scenario: Results are grouped by entity type
  Given AI is configured
  When the user submits a broad natural language query
  Then results are grouped into Contacts, Leads, Properties, and Transactions sections

@us153
Scenario: Natural language query falls back to keyword search when AI is not configured
  Given AI is not configured
  When the user types "hot leads from Zillow" in the search overlay
  Then a standard keyword search is performed with no error shown

@us153 @live_ai
Scenario: Real AI provider parses a natural language query and returns filtered results
  Given a real AI provider is configured
  And at least one lead with "Hot" status exists
  When the user types "show me my hot leads"
  Then the results include at least one Hot lead
```

## Manual Tests
**Story:** [US-186 — Search with Natural Language](../docs/174-natural-language-queries.md)

### Date range query returns records from the correct period
1. Open the global search overlay
2. Type "contacts added last month" and submit
3. Verify only contacts added in the previous calendar month are shown

### Status query filters leads correctly
1. Type "hot leads" in the search overlay
2. Verify only Hot-status leads appear in the results

### Results are grouped by entity type
1. Type a broad query (e.g., "Smith")
2. Verify results are separated into Contacts, Leads, Properties, and Transactions sections

### Falls back to keyword search when AI is not configured
1. Remove AI configuration
2. Type a natural language query in the search overlay
3. Verify a keyword search runs with no error message

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/ai.feature` |
| BDD step defs | `tests/bdd/test_ai.py` |
| Unit tests | `tests/unit/ai/test_natural_language_search.py` |
| Manual tests | `tests/manual/ai/natural-language-queries.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
