# US-065: Qualify a Lead with AI

## User Story

**As an** agent  
**I want to** qualify a lead using AI to get an assessment of their readiness to buy  
**So that** I can prioritize my follow-ups based on AI's analysis

## Priority

**MVP:** Must Have

**Rationale:** AI lead qualification is the flagship AI feature for MVP. It helps agents quickly assess which leads are most likely to convert based on their information, behavior, and responses. This saves time and helps agents focus on the hottest prospects.

## Estimated Effort

**Size:** Medium (M) - 3 days

**Breakdown:**
- 1 hour: Design qualification UI
- 2 hours: Implement AI prompt engineering for qualification
- 2 hours: Create qualification logic
- 1 hour: Add "Qualify with AI" button to lead details
- 1 hour: Handle AI provider errors gracefully
- 1 hour: Display qualification results
- 1 hour: Test with various lead data
- 1 hour: Test with different AI providers
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-064 (Configure AI Settings), US-030 (Create a New Lead), US-031 (View Lead List)

**Blocks:** US-066 (View AI Qualification Results), US-067 (Override AI Qualification)

## Description

Users should be able to trigger AI qualification for any lead. The AI analyzes the lead's information (budget, timeline, property preferences, notes, interactions) and provides an assessment of their readiness to buy, including a score, status (Hot/Warm/Cold), and reasoning.

The qualification should:
- Use the configured AI provider (Ollama or OpenAI)
- Analyze all available lead data
- Return a structured result (score, status, reasoning)
- Handle errors gracefully (AI unavailable, invalid data)
- Be triggerable with a button click
- Take a reasonable amount of time (under 30 seconds)

## BDD Scenarios

### Scenario 1: Trigger AI qualification

```
Given I am viewing a lead's details
  And AI is configured
When I click "Qualify with AI"
Then the AI should analyze the lead
  And show a progress indicator
  And display the results when complete
```

### Scenario 2: View qualification results

```
Given the AI has qualified a lead
When I view the results
Then I should see:
  - Qualification score (0-100)
  - Status (Hot/Warm/Cold)
  - Reasoning (why the AI gave this score)
  - Confidence level (optional)
```

### Scenario 3: AI analyzes lead data

```
Given a lead has the following data:
  - Budget: $400K-$500K
  - Timeline: 3 months
  - Status: Hot
  - Notes: "Pre-approved, actively looking"
When the AI qualifies this lead
Then the score should be high (80+)
  And the status should be "Hot"
  And the reasoning should mention pre-approval and active looking
```

### Scenario 4: AI handles incomplete data

```
Given a lead has minimal information
  (only name and email)
When the AI qualifies this lead
Then the score should be lower (uncertain)
  And the status should be "Cold" or "Warm"
  And the reasoning should note insufficient data
```

### Scenario 5: AI provider error

```
Given the AI provider is unavailable
When I try to qualify a lead
Then I should see a clear error message
  And the lead should not be marked as qualified
  And I should be able to retry
```

### Scenario 6: Qualification is saved

```
Given the AI has qualified a lead
When I view the lead later
Then the qualification results should be saved
  And I can see the score, status, and reasoning
  And when it was qualified
```

### Scenario 7: Re-qualify a lead

```
Given a lead has been qualified before
  And new information has been added
When I click "Qualify with AI" again
Then the AI should re-analyze with the new data
  And update the qualification results
```

### Scenario 8: AI qualification respects data privacy

```
Given I qualify a lead with AI
When the data is sent to the AI provider
Then only relevant lead data is sent
  And no sensitive information is unnecessarily shared
  And the data is sent securely (HTTPS)
```

## Manual Testing Steps

### Test 1: Trigger AI qualification

1. Configure AI provider (Ollama or OpenAI)
2. Create a lead with complete information
3. Open the lead's details
4. Click "Qualify with AI"
5. Verify the progress indicator appears
6. Wait for results
7. Verify the results are displayed

### Test 2: Test with different lead data

1. Create a lead with high-quality data (pre-approved, active timeline)
2. Qualify with AI
3. Verify the score is high
4. Create a lead with low-quality data (just browsing, no budget)
5. Qualify with AI
6. Verify the score is low
7. Compare the results

### Test 3: Test with incomplete data

1. Create a lead with only name and email
2. Qualify with AI
3. Verify the AI handles it gracefully
4. Verify the score reflects uncertainty
5. Verify the reasoning notes insufficient data

### Test 4: Test error handling

1. Disconnect from internet (for cloud AI)
2. Try to qualify a lead
3. Verify a clear error message
4. Reconnect to internet
5. Retry and verify it works

### Test 5: Test with invalid AI configuration

1. Configure AI with invalid API key
2. Try to qualify a lead
3. Verify the error message
4. Fix the configuration
5. Retry and verify it works

### Test 6: Test qualification persistence

1. Qualify a lead
2. Close the lead details
3. Reopen the lead
4. Verify the qualification results are saved
5. Verify the qualification date is shown

### Test 7: Test re-qualification

1. Qualify a lead
2. Add new information (e.g., increase budget)
3. Re-qualify the lead
4. Verify the results update
5. Verify the new qualification is saved

### Test 8: Test with different AI providers

1. Configure Ollama
2. Qualify a lead
3. Verify it works
4. Switch to OpenAI
5. Qualify a lead
6. Verify it works
7. Compare results from both providers

### Test 9: Test on all platforms

1. Test AI qualification on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] "Qualify with AI" button is available on lead details
- [ ] AI analyzes lead data and returns results
- [ ] Results include score, status, and reasoning
- [ ] Progress indicator shows during qualification
- [ ] AI handles incomplete data gracefully
- [ ] AI provider errors are handled with clear messages
- [ ] Qualification results are saved with the lead
- [ ] Leads can be re-qualified
- [ ] Qualification date is tracked
- [ ] Works with both Ollama and OpenAI
- [ ] Qualification completes in under 30 seconds
- [ ] Data privacy is respected
- [ ] Works on Windows, macOS, and Linux
- [ ] Results are accurate and useful