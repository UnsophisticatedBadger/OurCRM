# 70 - Create A New Lead

**Capability:** Leads
**Milestone:** MVP
**Status:** Not Done
**GitHub Issue:** #70

## User Story

As a real estate agent, I want to create a new lead with their details and preferences, so that I can track potential clients separately from general contacts.

## Dependencies

- #6 — Log In and Out (session factory registered in DI)
- #10 — Navigate Between Sections
- #56 — Create a New Contact (contact model used for lead-contact linking)

## Acceptance Criteria

1. "New Lead" button in the Leads section opens a form with fields for name, email, phone, status (Hot/Warm/Cold), source, budget min/max, desired location, property type, timeline, and notes
2. Name and status are required; saving with either empty shows an inline error and keeps the form open
3. If both budget fields are filled, min must not exceed max; saving with min > max shows "Minimum budget cannot be greater than maximum budget"
4. Saving a valid lead creates the lead record, creates or links a contact in the Contacts section with the same name/email/phone, returns to the lead list, and the new lead appears in it
5. Cancel closes the form without saving
6. Leads persist across application restarts

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/leads.feature`.

```gherkin
@story_70
Scenario: User creates a lead and sees it in the lead list
  Given the user is in the Leads section
  When the user clicks "New Lead", fills in name "Sara Lee" and status "Hot", and clicks Save
  Then the lead list shows "Sara Lee" with status "Hot"

@story_70
Scenario: User submits the lead form with no name and sees an error
  Given the new lead form is open
  When the user leaves the name empty and clicks Save
  Then an error is shown and the form stays open

@story_70
Scenario: User enters a min budget greater than max and sees an error
  Given the new lead form is open
  When the user enters min budget 500000 and max budget 300000 and clicks Save
  Then "Minimum budget cannot be greater than maximum budget" is shown

@story_70
Scenario: Creating a lead also creates a linked contact
  Given the user creates a lead "Sara Lee" with email "sara@example.com"
  When the user navigates to the Contacts section
  Then "Sara Lee" appears in the contact list

@story_70
Scenario: Lead persists after an application restart
  Given the user has created a lead "Sara Lee"
  When the application is restarted and the user opens the Leads section
  Then "Sara Lee" appears in the lead list
```

## Manual Tests

**Story:** [#70 — Create a New Lead](70-create-new-lead.md)
### User opens the new lead form and sees all fields
1. Navigate to the Leads section and click "New Lead"
2. Confirm the form shows fields for name, email, phone, status, source, budget min/max, desired location, property type, timeline, and notes

### User creates a lead with all fields filled
1. Fill in all fields with valid data and click Save
2. Confirm the lead list appears and the new lead is visible
3. Click the lead to confirm all data was saved correctly

### User sees an error for missing required fields
1. Leave name empty, select a status, and click Save — confirm an error appears
2. Enter a name but clear the status — confirm a status error appears

### Budget validation rejects min > max
1. Enter min $500,000 and max $300,000 and click Save
2. Confirm "Minimum budget cannot be greater than maximum budget" appears
3. Correct the values and confirm the lead saves

### Creating a lead also appears in Contacts
1. Create a lead with name and email
2. Navigate to the Contacts section
3. Confirm the contact appears with the same name and email

### Lead persists after restart
1. Create a lead, close the application, and restart
2. Navigate to Leads and confirm the lead is still there with all data intact

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/leads.feature` |
| BDD step defs | `tests/bdd/test_leads.py` |
| Unit tests | `tests/unit/leads/test_lead_form.py`, `test_lead_repository.py` |
| Manual tests | `tests/manual/leads/create_lead.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
- [ ] Wiki documentation written, or marked N/A with a reason
