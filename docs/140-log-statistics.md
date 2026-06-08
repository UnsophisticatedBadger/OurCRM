# US-140: Log Statistics

## User Story

**As a** developer or support user  
**I want to** view statistics about log files  
**So that** I can understand logging activity and identify potential issues

## Priority

**MVP:** Should Have

**Rationale:** Log statistics provide insights into application health: error rates, warning frequency, module activity. This helps identify problematic areas and monitor system health over time.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design statistics UI
- 1 hour: Implement log parsing for statistics
- 1 hour: Calculate statistics (counts by level, module, time)
- 1 hour: Display statistics
- 1 hour: Test statistics
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-122 (View Error Logs), US-139 (Log File Management)

**Blocks:** None

## Description

Users should be able to view statistics about log files including:
- Total log entries
- Count by log level (DEBUG, INFO, WARNING, ERROR)
- Count by module
- Error rate over time
- Most common errors
- Log file sizes

This helps identify problematic areas and monitor application health.

## BDD Scenarios

### Scenario 1: View log statistics

Given I am viewing the error logs When I click "View Statistics" Then I should see statistics including:

Total entries
Count by log level
Count by module
Time period covered

### Scenario 2: Statistics by log level

Given I have logs at various levels When I view statistics Then I should see counts for each level:

DEBUG: X
INFO: Y
WARNING: Z
ERROR: W

### Scenario 3: Statistics by module

Given I have logs from various modules When I view statistics Then I should see which modules generated the most logs And I can identify active/problematic modules


### Scenario 4: Error rate over time

Given I have logs over multiple days When I view statistics Then I should see error rate over time And I can identify trends (increasing/decreasing)


### Scenario 5: Most common errors

Given I have many error logs When I view statistics Then I should see the most common error messages And how many times each occurred


### Scenario 6: Log file sizes

Given I have multiple log files When I view statistics Then I should see the size of each log file And the total log storage used


### Scenario 7: Statistics for time period

Given I want statistics for a specific period When I select a date range Then the statistics should be for that period only


## Manual Testing Steps

### Test 1: View log statistics

1. Go to error logs
2. Click "View Statistics"
3. Verify statistics appear
4. Verify all metrics are shown

### Test 2: Test statistics by level

1. Generate logs at various levels
2. View statistics
3. Verify counts are accurate
4. Verify all levels are shown

### Test 3: Test statistics by module

1. Use various features (generate logs from different modules)
2. View statistics
3. Verify modules are listed
4. Verify counts are accurate

### Test 4: Test error rate over time

1. Have logs over multiple days
2. View statistics
3. Verify trends are shown
4. Verify you can see daily breakdown

### Test 5: Test most common errors

1. Generate many errors (some repeated)
2. View statistics
3. Verify most common are shown
4. Verify counts are accurate

### Test 6: Test file sizes

1. Have multiple log files
2. View statistics
3. Verify sizes are shown
4. Verify total is calculated

### Test 7: Test time period filter

1. View statistics
2. Select a date range
3. Verify statistics are filtered
4. Verify only that period is counted

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Log statistics are viewable
- [ ] Total entries are counted
- [ ] Count by log level is shown
- [ ] Count by module is shown
- [ ] Error rate over time is displayed
- [ ] Most common errors are listed
- [ ] Log file sizes are shown
- [ ] Total log storage is calculated
- [ ] Statistics can be filtered by date range
- [ ] Statistics are accurate
- [ ] Works on Windows, macOS, and Linux
- [ ] Statistics update when refreshed