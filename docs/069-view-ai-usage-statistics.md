# US-069: View AI Usage Statistics

## User Story

**As an** agent  
**I want to** view statistics about my AI usage  
**So that** I can understand how I'm using AI features and their value

## Priority

**MVP:** Should Have (could be deferred to post-MVP)

**Rationale:** Usage statistics help agents understand the value they're getting from AI features. While helpful, this is analytics/reporting that can be deferred to v0.2. The core AI qualification feature is more important for MVP.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design statistics UI
- 1 hour: Track AI usage metrics
- 1 hour: Calculate statistics
- 1 hour: Display usage data
- 1 hour: Show cost estimates (for cloud AI)
- 1 hour: Test statistics display
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-065 (Qualify a Lead with AI), US-064 (Configure AI Settings)

**Blocks:** None

## Description

Users should be able to view statistics about their AI usage, including how many leads they've qualified, how often they override the AI, which provider they use, and approximate costs (for cloud AI). This helps agents understand the value of AI features and make informed decisions about which provider to use.

Statistics should be displayed in a clear dashboard format and should be filterable by date range.

## BDD Scenarios

### Scenario 1: View AI usage statistics

```
Given I have used AI features
When I view the AI usage statistics
Then I should see:
  - Total leads qualified: X
  - Qualifications this month: Y
  - Overrides: Z (and override rate %)
  - Average AI response time
  - Provider used (Ollama/OpenAI)
```

### Scenario 2: View cost estimates (cloud AI)

```
Given I use OpenAI for AI features
When I view the statistics
Then I should see estimated costs:
  - Total API calls
  - Estimated cost this month
  - Cost per qualification
```

### Scenario 3: View override rate

```
Given I have qualified leads and made overrides
When I view the statistics
Then I should see:
  - Total qualifications: X
  - Overrides: Y
  - Override rate: Y/X%
  And this helps me understand AI accuracy
```

### Scenario 4: Filter statistics by date range

```
Given I have usage statistics
When I filter by date range (e.g., "This Month")
Then the statistics update to show only that period
  And I can see trends over time
```

### Scenario 5: View usage trends

```
Given I have been using AI features over time
When I view the statistics
Then I should see usage trends:
  - Daily/weekly/monthly usage
  - Most qualified days
  - Trends over time
```

### Scenario 6: Privacy of usage data

```
Given I view my usage statistics
When they are stored
Then they should be stored locally only
  And not sent to any external service
  And not used for any purpose other than displaying to me
```

### Scenario 7: No usage yet

```
Given I haven't used AI features yet
When I view the statistics
Then I should see an encouraging message
  Like "Start qualifying leads to see statistics"
```

### Scenario 8: Export statistics

```
Given I have usage statistics
When I click "Export"
Then I can export to CSV or PDF
  And it should include all metrics
```

## Manual Testing Steps

### Test 1: View statistics

1. Qualify several leads
2. Override some of them
3. View AI usage statistics
4. Verify all metrics are displayed
5. Verify the counts are accurate

### Test 2: Test cost estimates

1. Use OpenAI for qualifications
2. View statistics
3. Verify cost estimates are shown
4. Verify they're reasonable approximations
5. Test with different usage levels

### Test 3: Test override rate

1. Qualify 10 leads
2. Override 3 of them
3. View statistics
4. Verify the override rate is 30%
5. Verify the calculation is correct

### Test 4: Test date filtering

1. Use AI features over different time periods
2. View statistics
3. Filter by "This Month"
4. Verify only this month's data is shown
5. Test other date ranges

### Test 5: Test trends

1. Use AI features regularly
2. View statistics
3. Verify trends are shown
4. Verify the visualization is clear
5. Test over different time periods

### Test 6: Test privacy

1. View statistics
2. Check the database
3. Verify data is stored locally
4. Verify nothing is sent externally

### Test 7: Test empty state

1. Don't use any AI features
2. View statistics
3. Verify the encouraging message
4. Verify it's not discouraging

### Test 8: Test export

1. View statistics
2. Click "Export"
3. Choose format
4. Verify the export
5. Open the file
6. Verify all data is included

### Test 9: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] AI usage statistics are viewable
- [ ] Total qualifications are tracked
- [ ] Override rate is calculated
- [ ] Average response time is shown
- [ ] Provider usage is tracked
- [ ] Cost estimates shown for cloud AI
- [ ] Statistics can be filtered by date range
- [ ] Usage trends are visualized
- [ ] Usage data is stored locally only
- [ ] Empty state is encouraging
- [ ] Statistics can be exported
- [ ] Works on Windows, macOS, and Linux
- [ ] Statistics are accurate and useful