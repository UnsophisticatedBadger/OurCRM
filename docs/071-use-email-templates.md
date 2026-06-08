# US-071: Use Email Templates

## User Story

**As an** agent  
**I want to** use pre-built email templates for common scenarios  
**So that** I can send professional emails quickly without typing them from scratch

## Priority

**MVP:** Must Have

**Rationale:** Email templates save agents significant time. Instead of typing the same "Just Listed" announcement repeatedly, they can select a template, customize the details, and send. This is one of the most time-saving features for busy agents.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design template selection UI
- 2 hours: Create pre-built templates
- 1 hour: Implement template selection in compose form
- 1 hour: Add template variable substitution (e.g., {{name}}, {{address}})
- 1 hour: Add template preview
- 1 hour: Test template usage
- 1 hour: Test variable substitution
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-070 (Send Email to Contact), US-017 (Open Settings Window)

**Blocks:** US-072 (Email Logging in Contact Timeline), US-073 (Create Custom Email Templates - future)

## Description

Users should be able to select from a set of pre-built email templates when composing an email. Templates should include common real estate scenarios like "Just Listed", "Price Reduced", "Open House Invitation", "Follow-up After Showing", and "Thank You". Templates should support variable substitution (e.g., {{contact_name}}, {{property_address}}) that gets replaced with actual data from the contact or property.

The template system should make it easy to send professional, consistent emails with minimal effort. Users can preview the template before sending and make any necessary adjustments.

## BDD Scenarios

### Scenario 1: Select a template

```
Given the email compose form is open
When I click "Use Template"
Then I should see a list of available templates:
  - Just Listed
  - Price Reduced
  - Open House Invitation
  - Follow-up After Showing
  - Thank You
  - Market Update
  - Birthday Greeting
```

### Scenario 2: Apply template

```
Given I am composing an email
When I select the "Just Listed" template
Then the subject and body should be filled in
  And variables like {{contact_name}} should be replaced with the actual contact's name
  And variables like {{property_address}} should be replaced with the property address
```

### Scenario 3: Preview template

```
Given I have selected a template
When I click "Preview"
Then I should see how the email will look to the recipient
  And all variables should be replaced with actual data
  And the formatting should be clear
```

### Scenario 4: Edit template before sending

```
Given I have applied a template
When I edit the subject or body
Then my edits should be preserved
  And I can still send the customized email
```

### Scenario 5: Variable substitution

```
Given a template contains {{contact_name}} and {{property_address}}
When the template is applied to a contact and property
Then the variables should be replaced with:
  - {{contact_name}} → "John Smith"
  - {{property_address}} → "123 Main St, Houston, TX"
```

### Scenario 6: Multiple variables

```
Given a template has multiple variables:
  - {{contact_name}}
  - {{property_address}}
  - {{listing_price}}
  - {{agent_name}}
When the template is applied
Then all variables should be replaced correctly
  And no {{}} should remain in the sent email
```

### Scenario 7: Missing variable data

```
Given a template requires {{property_address}}
  But the email is not associated with a property
When the template is applied
Then the variable should be left blank or shown as "N/A"
  And a warning should be shown
  And the user can fill it in manually
```

### Scenario 8: Template categories

```
Given I am selecting a template
When I view the template list
Then templates should be organized by category:
  - Listing announcements
  - Follow-ups
  - Seasonal
  - Transaction updates
```

## Manual Testing Steps

### Test 1: Select a template

1. Open the email compose form
2. Click "Use Template"
3. Verify the template list appears
4. Verify all expected templates are present
5. Select a template
6. Verify it applies to the form

### Test 2: Test variable substitution

1. Open email compose for a contact
2. Select "Just Listed" template
3. Verify {{contact_name}} is replaced with the contact's name
4. Verify {{property_address}} is replaced with the property address
5. Verify all variables are replaced

### Test 3: Test preview

1. Apply a template
2. Click "Preview"
3. Verify the preview shows the formatted email
4. Verify all variables are replaced in the preview
5. Verify the formatting is clear

### Test 4: Test editing

1. Apply a template
2. Edit the subject
3. Edit the body
4. Verify the edits are preserved
5. Send the email
6. Verify the customized version was sent

### Test 5: Test multiple variables

1. Apply a template with multiple variables
2. Verify all are replaced correctly
3. Test with various contacts and properties
4. Verify consistency

### Test 6: Test missing data

1. Apply a template that requires property data
2. But don't associate a property
3. Verify the variable is handled gracefully
4. Verify a warning is shown
5. Fill in the data manually
6. Send the email

### Test 7: Test all pre-built templates

1. Test "Just Listed"
2. Test "Price Reduced"
3. Test "Open House Invitation"
4. Test "Follow-up After Showing"
5. Test "Thank You"
6. Test "Market Update"
7. Test "Birthday Greeting"
8. Verify all work correctly

### Test 8: Test on all platforms

1. Test templates on Windows
2. Verify they work
3. Test on macOS
4. Verify they work
5. Test on Linux
6. Verify they work
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] "Use Template" button is available in email compose
- [ ] Pre-built templates are available
- [ ] Templates cover common real estate scenarios
- [ ] Variables are substituted correctly
- [ ] Multiple variables work in one template
- [ ] Preview shows the formatted email
- [ ] Templates can be edited before sending
- [ ] Missing variable data is handled gracefully
- [ ] Templates are organized by category
- [ ] Professional, well-written template content
- [ ] Works on Windows, macOS, and Linux
- [ ] Templates save time and improve consistency
- [ ] Easy to use and understand