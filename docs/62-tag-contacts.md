# 62 - Tag Contacts

**Capability:** Contacts
**Milestone:** v0.5.0 — MVP
**Status:** Not Done
**GitHub Issue:** #62

## User Story

As a real estate agent, I want to add tags like "buyer" or "investor" to contacts, so that I can categorise them and find groups of people quickly.

## Dependencies

- #45 — View Contact Details

## Acceptance Criteria

1. The contact details view has a tag input; typing a label and pressing Enter adds it as a visible badge on the contact
2. Typing in the tag input shows autocomplete suggestions from tags already used across all contacts
3. Adding a tag the contact already has is prevented with a clear inline message
4. Clicking the X on a tag badge removes that tag from the contact
5. Tags are visible in both the contact details view and the contact list row
6. Tags persist across application restarts

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/contacts.feature`.

```gherkin
@story_54
Scenario: User adds a tag and it appears as a badge on the contact
  Given the user is viewing the details for "Jane Smith"
  When the user types "buyer" in the tag input and presses Enter
  Then a "buyer" badge is shown on the contact

@story_54
Scenario: User removes a tag
  Given "Jane Smith" has the tag "buyer"
  When the user clicks the X on the "buyer" badge
  Then the "buyer" badge is no longer shown

@story_54
Scenario: Adding a duplicate tag is prevented
  Given "Jane Smith" already has the tag "buyer"
  When the user types "buyer" in the tag input and presses Enter
  Then an error is shown and no duplicate badge is added

@story_54
Scenario: Existing tags appear as autocomplete suggestions
  Given another contact has the tag "investor"
  When the user types "inv" in the tag input on "Jane Smith"
  Then "investor" appears as a suggestion

@story_54
Scenario: Tags persist after an application restart
  Given "Jane Smith" has the tag "buyer"
  When the application is restarted and the user opens "Jane Smith"
  Then the "buyer" badge is shown
```

## Manual Tests

**Story:** [#49 — Tag Contacts](../docs/012-tag-contacts.md)

### User adds a tag and sees it as a badge
1. Open any contact's details
2. Type "buyer" in the tag input and press Enter
3. Confirm a "buyer" badge appears on the contact
4. Navigate to the contact list and confirm the badge is also visible in the row

### User adds multiple tags
1. Add "buyer", "investor", and "referral" to a contact
2. Confirm all three badges appear
3. Confirm the layout looks clean with multiple badges

### User removes a tag
1. Click the X on the "buyer" badge
2. Confirm the badge disappears immediately
3. Confirm the contact's other tags are unchanged

### Autocomplete suggests existing tags
1. Ensure at least one other contact has the tag "investor"
2. Open the tag input on a different contact and type "inv"
3. Confirm "investor" appears as a suggestion
4. Select the suggestion and confirm it is added as a badge

### Duplicate tags are prevented
1. Add "buyer" to a contact
2. Try to add "buyer" again
3. Confirm an error appears and no second "buyer" badge is created

### Tags persist after restart
1. Tag a contact with "buyer" and "seller"
2. Close and restart the application
3. Open the contact and confirm both tags are still shown

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/contacts.feature` |
| BDD step defs | `tests/bdd/test_contacts.py` |
| Unit tests | `tests/unit/contacts/test_contact_tags.py` |
| Manual tests | `tests/manual/contacts/tag_contact.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
