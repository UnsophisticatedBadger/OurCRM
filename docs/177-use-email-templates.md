# 177 - Use Email Templates

**Capability:** Email
**Milestone:** Post-Production
**Status:** Not Done
**GitHub Issue:** #177

## User Story

As a real estate agent, I want to select a pre-built email template when composing an email, so that I can send professional, consistent messages quickly without writing them from scratch.

## Dependencies

- #126 — Send Email to Contact

## Acceptance Criteria

1. A "Use Template" button is available in the email compose form
2. Clicking it presents a list of pre-built real estate templates covering common scenarios (e.g., Just Listed, Price Reduced, Open House Invitation, Follow-up After Showing, Thank You, Market Update)
3. Selecting a template populates the subject and body fields with the template content
4. Supported variables ({{contact_name}}, {{property_address}}, {{listing_price}}, {{agent_name}}) are substituted with the corresponding data available in the current compose context
5. When a variable cannot be resolved (e.g., no property is linked), the placeholder is replaced with an empty string and a warning lists the unresolved variables so the agent can fill them in manually
6. The subject and body remain fully editable after a template is applied

## BDD Scenarios

> These scenarios are not yet implemented. Add them to `tests/bdd/features/email.feature`.

```gherkin
@story_177
Scenario: User selects a template and the compose form is populated
  Given the email compose form is open
  When the user clicks "Use Template" and selects "Follow-up After Showing"
  Then the subject field is populated with the template's subject line
  And the body field is populated with the template's body text

@story_177
Scenario: Variable substitution replaces placeholders with contact data
  Given the compose form is open for contact "Alice Smith"
  And the "Follow-up After Showing" template contains {{contact_name}}
  When the user applies the template
  Then the body shows "Alice Smith" where {{contact_name}} appeared

@story_177
Scenario: Unresolvable variable is replaced with empty string and a warning is shown
  Given the compose form is open with no property linked
  And the "Just Listed" template contains {{property_address}}
  When the user applies the template
  Then {{property_address}} is replaced with an empty string in the body
  And a warning lists "property_address" as unresolved

@story_177
Scenario: User edits the body after applying a template and the edits are preserved
  Given a template has been applied to the compose form
  When the user modifies the body text
  Then the modified text is retained
  And clicking Send transmits the edited version
```

## Manual Tests

**Story:** [#127 — Use Email Templates](../docs/080-use-email-templates.md)

### Template selection populates subject and body
1. Open the email compose form
2. Click "Use Template" and confirm a list of pre-built templates is shown
3. Select "Follow-up After Showing"
4. Confirm the subject and body fields are populated with the template content

### Variable substitution replaces known placeholders
1. Open the compose form for a contact with a known name (e.g., "Alice Smith")
2. Apply a template containing {{contact_name}}
3. Confirm "Alice Smith" appears in place of the placeholder
4. If agent name data is available, confirm {{agent_name}} is also replaced

### Unresolvable variable warning
1. Open the compose form without a property linked
2. Apply a template that contains {{property_address}}
3. Confirm a warning lists "property_address" as unresolved
4. Confirm the placeholder is empty (not "{{property_address}}") in the body
5. Manually fill in the address and send successfully

### Template body remains editable
1. Apply any template
2. Modify the subject and body
3. Confirm the edited content is what appears in the compose form
4. Send the email and confirm the edited version was transmitted (check recipient's inbox)

## Test Locations

| Artifact | Path |
|----------|------|
| BDD feature | `tests/bdd/features/email.feature` |
| BDD step defs | `tests/bdd/test_email.py` |
| Unit tests | `tests/unit/email/test_email_templates.py` |
| Manual tests | `tests/manual/email/email_templates.md` |

## Definition of Done

- [ ] BDD scenarios pass end-to-end
- [ ] Feature reachable from the running app
- [ ] `ruff`, `mypy --strict` clean
- [ ] Manual tests documented and verified
