# Edit A Lead — Manual Tests

**Story:** [#72 — Edit a Lead](../../../docs/72-edit-a-lead.md)

## User opens the edit form and sees all fields pre-populated
1. Open any lead's details and click Edit
2. Confirm every field is pre-populated with the lead's current data
3. Confirm the form title distinguishes editing from creating

## User edits status and sees it reflected in details and list
1. Change the status to "Hot" and save
2. Confirm the details view shows "Hot" with the red indicator
3. Navigate back to the list and confirm the row also shows "Hot"

## Budget validation rejects min > max
1. Enter min $600,000 and max $400,000, click Save
2. Confirm "Minimum budget cannot be greater than maximum budget" appears
3. Fix the values and confirm the lead saves

## Budget range is displayed formatted after editing
1. Set budget min $300,000 and max $500,000 and save
2. Confirm the details and list both show "$300,000 – $500,000"

## Custom source via "Other"
1. Select "Other" from the source dropdown
2. Confirm a free-text field appears
3. Enter "Neighbourhood flyer" and save
4. Confirm the lead shows "Neighbourhood flyer" as the source

## Cancel discards changes
1. Open the edit form and change several fields
2. Click Cancel
3. Confirm the details view still shows the original data

## Status can be changed from the list without opening the edit form
1. Right-click a lead in the list and choose "Change Status"
2. Select a new status
3. Confirm the row updates immediately without navigating away

## All edits survive a restart
1. Edit a lead's status, budget, and source, then save
2. Close the application and restart
3. Open the lead and confirm all changes are still shown
