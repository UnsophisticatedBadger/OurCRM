# Move Lead Through Pipeline — Manual Tests

**Story:** [#73 — Move Lead Through Pipeline](../../../docs/73-move-lead-through-pipeline.md)

## User sees the current pipeline stage in lead details
1. Open any lead's details view
2. Confirm a stage field is visible showing one of the eight defined stages
3. Confirm the stage is separate from the Hot/Warm/Cold status

## User advances a lead through stages
1. Open a lead in "New Lead" stage
2. Change the stage to "Contacted" and save
3. Confirm the details view shows "Contacted"
4. Navigate to the lead list and confirm the stage column also shows "Contacted"

## User marks a lead as Lost with a reason
1. Change a lead's stage to "Lost"
2. Confirm an optional reason text field appears
3. Enter a reason and save
4. Confirm the lead shows "Lost" with the reason visible

## User moves a lead backward in the pipeline
1. Open a lead in "Offer Made" stage
2. Change the stage back to "Qualified" and save
3. Confirm the stage updates to "Qualified" without error

## Stage column is visible in the lead list
1. Create leads with different pipeline stages
2. Open the lead list and confirm the stage column shows each lead's current stage

## Stage persists after a restart
1. Set a lead's stage to "Under Contract" and save
2. Close the application and restart
3. Open the lead and confirm the stage is still "Under Contract"

## User marks a lead as Lost without entering a reason
1. Change a lead's stage to "Lost"
2. Leave the reason field blank and save
3. Confirm the lead shows stage "Lost" with no reason displayed

## Reason is cleared after a lead is moved off the Lost stage
1. Set a lead's stage to "Lost" with a reason and save
2. Change the stage to any other stage and save
3. Confirm the reason no longer appears anywhere for that lead

## A newly created lead starts in the New Lead stage
1. Create a new lead without touching the stage selector
2. Confirm the details view shows stage "New Lead"

## Changing a lead's stage does not affect its status
1. Open a lead with status "Hot"
2. Change its stage and save
3. Confirm the status still shows "Hot"
