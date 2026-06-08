# US-067: Override AI Qualification

## User Story

**As an** agent  
**I want to** override the AI's qualification with my own assessment  
**So that** I can use my judgment when I disagree with the AI

## Priority

**MVP:** Must Have

**Rationale:** AI is a tool to assist agents, not replace their judgment. Agents often have context the AI doesn't (personal interactions, intuition, local market knowledge). They need the ability to override AI assessments with their own, while keeping the AI's recommendation visible for reference.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design override UI
- 1 hour: Implement manual status change after AI qualification
- 1 hour: Show both AI and manual assessments
- 1 hour: Add notes for override reason
- 1 hour: Track who made the final decision
- 1 hour: Test override flow
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-066 (View AI Qualification Results), US-031 (View Lead List)

**Blocks:** US-068 (View Qualification History)

## Description

When an agent disagrees with the AI's qualification, they should be able to override it with their own assessment. The override should be saved along with the AI's original recommendation, so the agent can see both. The agent can also add notes explaining why they overrode the AI.

The lead's status should update to the agent's chosen value, but the AI's score and reasoning should remain visible for reference. This creates a feedback loop where the agent's judgment is respected while preserving the AI's input.

## BDD Scenarios

### Scenario 1: Override AI qualification

```
Given a lead has been qualified by AI
  And I disagree with the AI's assessment
When I change the lead's status manually
  And optionally add a note explaining why
  And I save the change
Then the lead's status should update to my chosen value
  And the AI's original qualification should still be visible
  And my override should be marked as the final decision
```

### Scenario 2: View both AI and manual assessments

```
Given a lead has been qualified by AI
  And I have overridden the qualification
When I view the lead's details
Then I should see:
  - My manual status (prominently displayed)
  - The AI's original assessment (for reference)
  - My override notes (if provided)
  - When the override was made
```

### Scenario 3: Add override notes

```
Given I am overriding the AI's qualification
When I add notes explaining my reasoning
  And I save the change
Then the notes should be saved
  And they should be visible in the lead's history
```

### Scenario 4: AI assessment is preserved

```
Given I have overridden the AI's qualification
When I view the lead's details
Then the AI's original score and reasoning should still be shown
  And it should be clear that the AI's assessment was overridden
```

### Scenario 5: Override is tracked

```
Given I have overridden the AI's qualification
When I view the qualification history
Then the override should be logged
  And it should show what the AI said
  And what I changed it to
  And why
```

### Scenario 6: Manual status change without AI

```
Given a lead has not been qualified by AI
When I manually set the status
Then it should work the same as any other status change
  And no AI override is needed
```

### Scenario 7: Re-qualify after override

```
Given I have overridden the AI's qualification
When I re-qualify the lead with AI
Then the AI should analyze again
  And the new results should replace the old AI results
  And my previous override should be noted in history
```

### Scenario 8: Visual indicator of override

```
Given a lead's status was set by overriding the AI
When I view the lead's details
Then there should be a visual indicator that this is a manual override
  And the AI's recommendation should be shown differently
```

## Manual Testing Steps

### Test 1: Override AI qualification

1. Qualify a lead with AI
2. Note the AI's assessment
3. Change the status manually
4. Add override notes
5. Save the change
6. Verify the status updated
7. Verify the AI's assessment is still visible

### Test 2: Test viewing both assessments

1. Qualify a lead with AI
2. Override the qualification
3. View the lead's details
4. Verify both AI and manual assessments are shown
5. Verify it's clear which is which

### Test 3: Test override notes

1. Qualify a lead with AI
2. Override with detailed notes
3. Save the change
4. View the notes
5. Verify they're saved and visible

### Test 4: Test AI assessment preservation

1. Qualify a lead with AI
2. Override the qualification
3. Close and reopen the lead
4. Verify the AI's original assessment is still there
5. Verify it's marked as overridden

### Test 5: Test override tracking

1. Qualify and override a lead
2. View the qualification history
3. Verify the override is logged
4. Verify all details are captured (AI said X, I changed to Y, because Z)

### Test 6: Test manual status without AI

1. Create a new lead
2. Don't qualify with AI
3. Manually set the status
4. Verify it works normally
5. Verify no override is needed

### Test 7: Test re-qualify after override

1. Qualify and override a lead
2. Re-qualify with AI
3. Verify the new AI results
4. Verify the override history is preserved

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Agent can override AI qualification manually
- [ ] Override can include explanatory notes
- [ ] AI's original assessment remains visible
- [ ] Manual status is clearly marked as the final decision
- [ ] Override is tracked in history
- [ ] Visual indicator shows when status is a manual override
- [ ] Re-qualification works after override
- [ ] Manual status changes work without AI qualification
- [ ] Works on Windows, macOS, and Linux
- [ ] Override flow is intuitive
- [ ] Agent's judgment is respected
- [ ] AI and manual assessments are both preserved