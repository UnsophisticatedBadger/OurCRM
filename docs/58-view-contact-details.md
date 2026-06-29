# 58 - View Contact Details

**Capability:** Contacts
**Milestone:** v0.5.0 — MVP
**Status:** Not Done
**GitHub Issue:** #58

## User Story

As a real estate agent, I want to open a contact and see all their information on one screen, so that I have everything I need before calling or meeting them.

## Dependencies

- #44 — View Contact List

## Acceptance Criteria

1. Double-clicking a contact in the list opens a details view showing all stored fields; fields with no data show "Not provided"
2. The details view has Edit, Delete, and Add Note action buttons
3. Previous and Next buttons navigate between contacts in the current list order
4. "Back to List" button and the Escape key return to the contact list with the same contact still selected

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/contacts.feature`.

```gherkin
@story_58
Scenario: User opens a contact and sees all stored fields
  Given a contact "Jane Smith" exists with email "jane@example.com" and phone "555-1234"
  When the user double-clicks "Jane Smith" in the contact list
  Then the details view shows "jane@example.com" and "555-1234"

@story_58
Scenario: User sees "Not provided" for empty optional fields
  Given a contact "Bob Carter" exists with only a name
  When the user opens the details for "Bob Carter"
  Then empty optional fields show "Not provided"

@story_58
Scenario: User navigates to the next contact
  Given the user is viewing details for "Alice Brown" with "Bob Carter" next in list order
  When the user clicks Next
  Then the details for "Bob Carter" are shown

@story_58
Scenario: User returns to the list and the same contact is still selected
  Given the user is viewing the details for "Alice Brown"
  When the user clicks Back to List
  Then the contact list is shown with "Alice Brown" still selected
```

## Manual Tests

**Story:** [#45 — View Contact Details](../docs/012-view-contact-details.md)

### User opens a contact and sees all their data
1. Create a contact with all fields filled
2. Double-click the contact in the list
3. Confirm all fields display the correct values
4. Confirm empty optional fields show "Not provided"

### User navigates between contacts with Previous and Next
1. Create 3 contacts (A, B, C sorted by name)
2. Open contact A
3. Click Next — confirm contact B is shown
4. Click Next — confirm contact C is shown
5. Click Previous — confirm contact B is shown again

### User returns to the list with the same contact selected
1. Open the details for a contact
2. Click "Back to List"
3. Confirm the contact list appears
4. Confirm the contact you were viewing is still highlighted/selected
5. Repeat using the Escape key — confirm the same result

### Edit, Delete, and Add Note buttons are present
1. Open any contact's details
2. Confirm Edit, Delete, and Add Note buttons are visible
3. Click each and confirm they open the expected flow (edit form, delete confirmation, note input)

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/contacts.feature` |
| BDD step defs | `tests/bdd/test_contacts.py` |
| Unit tests | `tests/unit/contacts/test_contact_details.py` |
| Manual tests | `tests/manual/contacts/contact_details.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
