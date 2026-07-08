# 65 - Search Contacts Across All Fields

**Capability:** Contacts
**Milestone:** MVP
**Status:** Not Done
**GitHub Issue:** #65

## User Story

As a real estate agent, I want the contact search to also look through notes, tags, and address fields, so that I can find a contact even when I only remember something they told me or a tag I assigned them.

## Dependencies

- #52 — Search Contacts
- #48 — Add Notes to a Contact
- #50 — Tag Contacts

## Acceptance Criteria

1. The existing contact search (#52) also matches against notes, tags, and address fields
2. Name and email matches rank above notes and tag matches so the most direct results appear first
3. Matching text is highlighted in the search results so users can see why each contact matched
4. An empty search box shows all contacts (unchanged from #52)

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/contacts.feature`.

```gherkin
@story_65
Scenario: User finds a contact by searching note content
  Given "Jane Smith" has a note containing "conference"
  When the user searches for "conference"
  Then "Jane Smith" appears in results

@story_65
Scenario: User finds contacts by searching a tag name
  Given "Bob Carter" has the tag "investor"
  When the user searches for "investor"
  Then "Bob Carter" appears in results

@story_65
Scenario: User finds a contact by searching an address field
  Given a contact with city "Houston" exists
  When the user searches for "Houston"
  Then that contact appears in results

@story_65
Scenario: Name matches rank above note matches
  Given "John Smith" exists and "Jane Doe" has a note mentioning "John"
  When the user searches for "John"
  Then "John Smith" appears above "Jane Doe" in results
```

## Manual Tests

**Story:** [#53 — Search Contacts Across All Fields](../docs/025-search-across-all-fields.md)

### User finds a contact via a note keyword
1. Add the note "Met at Houston conference" to a contact
2. Search for "conference"
3. Confirm the contact appears in results even though "conference" is not in their name, email, or phone

### User finds contacts via a tag
1. Tag two contacts with "investor"
2. Search for "investor"
3. Confirm both contacts appear in results

### User finds a contact via address
1. Create a contact with city "Houston"
2. Search for "Houston"
3. Confirm the contact appears in results

### Name matches appear before note matches
1. Create "John Smith" (name match)
2. Create "Jane Doe" with a note that mentions "John"
3. Search for "John"
4. Confirm "John Smith" appears above "Jane Doe"

### Matching text is highlighted
1. Search for a term that matches a note or tag
2. Confirm the matching text is visually highlighted in the results so it is clear why the contact matched

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/contacts.feature` |
| BDD step defs | `tests/bdd/test_contacts.py` |
| Unit tests | `tests/unit/contacts/test_contact_full_text_search.py` |
| Manual tests | `tests/manual/contacts/search_all_fields.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
