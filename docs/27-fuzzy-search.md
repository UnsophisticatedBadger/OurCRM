# 27 - Fuzzy Search

**Capability:** shell
**Milestone:** Secure Shell
**Status:** Not Done
**GitHub Issue:** #27
**Priority:** Post-MVP

## User Story
As an agent, I want search to find records even when I misspell a name or term, so that I can locate people and records quickly without worrying about exact spelling.

## Dependencies
- #64 — Search Contacts
- #16 — Search Contacts Globally

## Acceptance Criteria
1. Search tolerates up to 2 character substitutions, insertions, or deletions (edit distance ≤ 2) and still returns the matching record
2. Phonetically similar names are matched (e.g. "Smyth" finds "Smith")
3. Partial string matches are supported (e.g. "John" matches "Johnson")
4. Exact matches are ranked above fuzzy matches in results
5. Fuzzy match results are visually distinguished from exact matches (e.g. a "fuzzy match" label)
6. Fuzzy matching applies across name, email, phone, and address fields
7. User can disable fuzzy search from Settings → Search; when disabled only exact and prefix matches are returned
8. A fuzzy match threshold (Strict / Normal / Loose) is configurable from Settings → Search

## BDD Scenarios
> These scenarios are not yet implemented. Add them to `tests/bdd/features/shell.feature`.

```gherkin
@story_27
Scenario: Search with a one-character typo still finds the contact
  Given a contact named "Johnson" exists
  When the user searches for "Jonson"
  Then "Johnson" appears in the results
  And the result is labelled as a fuzzy match

@story_27
Scenario: Phonetically similar name finds the matching contact
  Given a contact named "Smith" exists
  When the user searches for "Smyth"
  Then "Smith" appears in the results

@story_27
Scenario: Exact matches are ranked above fuzzy matches
  Given contacts named "Johnson" and "Jonson" both exist
  When the user searches for "Johnson"
  Then "Johnson" (exact match) appears before "Jonson" (fuzzy match) in the results

@story_27
Scenario: Fuzzy search can be disabled in Settings
  Given the user has disabled fuzzy search in Settings → Search
  When the user searches for "Jonson"
  Then "Johnson" does not appear in the results

@story_27
Scenario: Threshold set to Strict requires a closer match
  Given the fuzzy threshold is set to "Strict"
  When the user searches for a term with 2 character differences from a contact's name
  Then the contact is not returned
```

## Manual Tests
**Story:** [#27 — Fuzzy Search](27-fuzzy-search.md)
### One-character typo still finds the contact
1. Create a contact named "Johnson"
2. Search for "Jonson"
3. Verify "Johnson" appears in results labelled as a fuzzy match

### Phonetic match finds the contact
1. Search for "Smyth"
2. Verify "Smith" appears in the results

### Exact matches rank above fuzzy matches
1. Ensure contacts "Johnson" and "Jonson" both exist
2. Search for "Johnson" and verify the exact match appears first

### Disabling fuzzy search excludes near-matches
1. Disable fuzzy search in Settings → Search
2. Search for "Jonson" and verify "Johnson" does not appear

## Test Locations
| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/shell.feature` |
| BDD step defs | `tests/bdd/test_shell.py` |
| Unit tests | `tests/unit/shell/test_fuzzy_search.py` |
| Manual tests | `tests/manual/shell/fuzzy-search.md` |

## Definition of Done
- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
