# Create A New Lead — Manual Tests

**Story:** [#70 — Create a New Lead](../../../docs/70-create-new-lead.md)

## User opens the new lead form and sees all fields
1. Navigate to the Leads section and click "New Lead"
2. Confirm the form shows fields for name, email, phone, status, source, budget min/max, desired location, property type, timeline, and notes

## User creates a lead with all fields filled
1. Fill in all fields with valid data and click Save
2. Confirm the lead list appears and the new lead is visible
3. Click the lead to confirm all data was saved correctly

## User sees an error for missing required fields
1. Leave name empty, select a status, and click Save — confirm an error appears
2. Enter a name but clear the status — confirm a status error appears

## Budget validation rejects min > max
1. Enter min $500,000 and max $300,000 and click Save
2. Confirm "Minimum budget cannot be greater than maximum budget" appears
3. Correct the values and confirm the lead saves

## Creating a lead also appears in Contacts
1. Create a lead with name and email
2. Navigate to the Contacts section
3. Confirm the contact appears with the same name and email

## Creating a lead for an existing contact reuses that contact
1. Create a contact "Sara Lee" with email "sara@example.com" in the Contacts section
2. Create a new lead with the same name and email
3. Navigate to Contacts and confirm there is still only one "Sara Lee" contact, not a duplicate

## User cancels the form and nothing is saved
1. Click "New Lead", fill in some fields, and click Cancel
2. Confirm the form closes
3. Confirm no new lead appears in the lead list

## Lead persists after restart
1. Create a lead, close the application, and restart
2. Navigate to Leads and confirm the lead is still there with all data intact
