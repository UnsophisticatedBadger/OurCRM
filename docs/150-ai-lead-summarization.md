# US-150: AI Lead Summarization

## User Story

**As an** agent  
**I want to** get AI-generated summaries of lead history  
**So that** I can quickly understand a lead's background before calling or meeting

## Priority

**Future:** Post-MVP

**Rationale:** Agents often need to quickly review a lead's history before interactions. AI summarization condenses all notes, emails, showings, and activities into a concise summary, saving preparation time.

## Estimated Effort

**Size:** Medium (M) - 3-5 days

**Breakdown:**
- 2 hours: Design summary UI
- 3 hours: Implement AI summarization logic
- 2 hours: Gather lead data for context
- 2 hours: Display summary in lead details
- 2 hours: Test summarization quality
- 2 hours: Test on all platforms

## Dependencies

**Depends on:** US-064 (Configure AI Settings), US-031 (View Lead List)

**Blocks:** None

## Description

Users should be able to generate an AI summary of any lead's history. The summary includes:
- Key interactions (calls, emails, showings)
- Preferences and requirements
- Current status and timeline
- Any concerns or objections raised
- Recommended next steps

The summary is generated on-demand and can be refreshed as new information is added.

## BDD Scenarios

### Scenario 1: Generate lead summary

Given I am viewing a lead's details And AI is configured When I click "Generate Summary" Then an AI summary should be generated Including key interactions and preferences


### Scenario 2: Summary includes all interactions

Given a lead has emails, notes, and showings When I generate a summary Then all interactions should be summarized In chronological context


### Scenario 3: Summary highlights preferences

Given a lead has stated preferences When I generate a summary Then preferences should be highlighted Like budget, location, property type


### Scenario 4: Summary suggests next steps

Given I generate a lead summary Then it should include recommended next steps Based on the lead's status and activity


### Scenario 5: Refresh summary

Given I have generated a summary When new activity occurs And I click "Refresh Summary" Then the summary should be updated With the new information


### Scenario 6: Summary length options

Given I am generating a summary When I choose summary length Then I can select:

Brief (2-3 sentences)
Standard (paragraph)
Detailed (full summary)

### Scenario 7: Copy summary to clipboard

Given I have generated a summary When I click "Copy Summary" Then the summary should be copied And I can paste it elsewhere


### Scenario 8: Summary is accurate

Given I generate a lead summary When I review it Then it should accurately reflect the lead's history Without hallucinations or errors


## Manual Testing Steps

### Test 1: Generate lead summary

1. Open a lead's details
2. Click "Generate Summary"
3. Verify summary is created
4. Verify it's accurate

### Test 2: Test interaction coverage

1. Create lead with various interactions
2. Generate summary
3. Verify all are mentioned

### Test 3: Test preferences highlighted

1. Add lead preferences
2. Generate summary
3. Verify they're highlighted

### Test 4: Test next steps

1. Generate summary
2. Verify next steps are suggested
3. Verify they're relevant

### Test 5: Test refresh

1. Generate summary
2. Add new activity
3. Refresh summary
4. Verify it's updated

### Test 6: Test length options

1. Generate brief summary
2. Generate detailed summary
3. Verify length differs

### Test 7: Test copy to clipboard

1. Generate summary
2. Click "Copy Summary"
3. Paste elsewhere
4. Verify it works

### Test 8: Test on all platforms

1. Test Windows, macOS, Linux
2. Verify all work

## Acceptance Criteria

- [ ] "Generate Summary" button in lead details
- [ ] Summary includes all interactions
- [ ] Preferences are highlighted
- [ ] Current status is summarized
- [ ] Next steps are recommended
- [ ] Can choose summary length
- [ ] Can refresh summary
- [ ] Can copy summary to clipboard
- [ ] Summary is accurate (no hallucinations)
- [ ] Works with Ollama and OpenAI
- [ ] Works on Windows, macOS, and Linux
- [ ] Summary generation completes in under 10 seconds