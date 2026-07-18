# 56 - Create A New Contact

**Capability:** Contacts
**Milestone:** MVP
**Status:** Done
**GitHub Issue:** #56

## User Story

As a real estate agent, I want to create a new contact with basic information, so that I can track the people I work with.

## Dependencies

- #6 — Log In and Out (session factory registered in DI)
- #10 — Navigate Between Sections

## Acceptance Criteria

1. "New Contact" button in the Contacts section opens a blank form with fields for first name, last name, email, phone, address (street, city, state, ZIP), and notes
2. First name or last name is required; submitting with both empty shows "Name is required" and keeps the form open
3. Email and phone are validated on save; invalid formats show an inline field error
4. Saving a valid contact closes the form, returns to the contact list, and the new contact appears in it
5. Cancel closes the form without saving; no contact is created
6. Created contacts persist across application restarts

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/contacts.feature`.

```gherkin
@story_56
Scenario: User creates a contact with a name and sees it in the list
  Given the user is in the Contacts section
  When the user clicks "New Contact"
  And fills in first name "Jane" and last name "Smith"
  And clicks Save
  Then the contact list shows "Jane Smith"

@story_56
Scenario: User submits the new contact form with no name and sees an error
  Given the new contact form is open
  When the user leaves both name fields empty and clicks Save
  Then the error "Name is required" is shown
  And the form stays open

@story_56
Scenario: User enters an invalid email and sees a validation error
  Given the new contact form is open
  When the user enters "notanemail" in the email field and clicks Save
  Then an inline email format error is shown

@story_56
Scenario: User cancels the new contact form and no contact is created
  Given the new contact form is open and the user has entered data
  When the user clicks Cancel
  Then the form closes and the contact does not appear in the contact list

@story_56
Scenario: Contact created in one session is visible after restart
  Given the user has created a contact "Jane Smith"
  When the application is restarted and the user opens the Contacts section
  Then "Jane Smith" appears in the contact list
```

## Manual Tests

**Story:** [#56 — Create a New Contact](56-create-new-contact.md)
### User opens the new contact form
1. Navigate to the Contacts section
2. Click "New Contact"
3. Confirm the form opens with all expected fields present and empty

### User creates a contact with all fields filled
1. Open the new contact form
2. Fill in all fields with valid data
3. Click Save
4. Confirm the contact list appears and the new contact is visible
5. Click the contact to confirm all data was saved correctly

### User submits the form with an empty name and sees an error
1. Open the new contact form
2. Leave first and last name empty, fill in other fields
3. Click Save
4. Confirm "Name is required" appears and the form stays open
5. Enter a name and confirm the form can now be saved

### User enters an invalid email and sees a validation error
1. Open the new contact form, enter "notanemail" in the email field
2. Click Save
3. Confirm an email format error appears inline
4. Correct the email and confirm the error clears

### User cancels and confirms nothing was saved
1. Open the new contact form and fill in a name
2. Click Cancel
3. Confirm the form closes and the contact does not appear in the list

### Contact persists after restart
1. Create a contact, close the application
2. Restart and navigate to Contacts
3. Confirm the contact is still there with all fields intact

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/contacts.feature` |
| BDD step defs | `tests/bdd/test_contacts.py` |
| Unit tests | `tests/unit/contacts/test_contact_form.py`, `test_contact_repository.py`, `test_contact_validator.py`, `test_contacts_page.py` |
| Manual tests | `tests/manual/contacts/create_contact.md` |

## Definition of Done

- [x] BDD scenarios pass end-to-end
- [x] Feature reachable from the running app
- [x] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [x] Wiki documentation written, or marked N/A with a reason
