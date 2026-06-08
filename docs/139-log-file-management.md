# US-139: Log File Management

## User Story

**As a** developer or support user  
**I want to** manage log files (rotation, size limits, cleanup)  
**So that** logs don't consume unlimited disk space and remain useful for debugging

## Priority

**MVP:** Should Have

**Rationale:** Without log management, log files can grow indefinitely and consume disk space. Log rotation ensures old logs are archived or deleted, keeping the system healthy while maintaining recent logs for debugging.

## Estimated Effort

**Size:** Small (S) - 2 days

**Breakdown:**
- 1 hour: Design log management settings
- 2 hours: Implement log rotation
- 1 hour: Implement size limits
- 1 hour: Implement automatic cleanup
- 1 hour: Test log management
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-008 (Create First Test), US-122 (View Error Logs)

**Blocks:** None

## Description

The logging system should include:
1. **Log rotation**: Create new log file daily or when size limit reached
2. **Size limits**: Maximum total log storage (e.g., 100MB)
3. **Automatic cleanup**: Delete old logs beyond retention period
4. **Configurable retention**: User can set how many days to keep logs

Logs should be stored in a dedicated folder with clear naming (e.g., `ourcrm-2024-01-15.log`).

## BDD Scenarios

### Scenario 1: Log rotation by size

Given the current log file reaches the size limit When a new log entry is written Then a new log file should be created And the old file should be archived or deleted


### Scenario 2: Log rotation by time

Given it is a new day When the application writes a log entry Then a new log file should be created for the new day And the old file should be preserved


### Scenario 3: Automatic cleanup of old logs

Given there are logs older than the retention period When the application starts Then old logs should be automatically deleted And only logs within retention period should remain


### Scenario 4: Configure log retention

Given I am in Settings When I set the log retention period And I save the settings Then logs should be kept for that many days And older logs should be deleted


### Scenario 5: Maximum log storage

Given the total log storage reaches the maximum When a new log is written Then the oldest logs should be deleted And the total should stay within the limit


### Scenario 6: Manual log cleanup

Given I am viewing error logs When I click "Clear Old Logs" Then logs older than retention period should be deleted And I should see how much space was freed


### Scenario 7: Log file naming

Given logs are being created When I examine the log files Then they should have clear names with dates And be easy to identify


## Manual Testing Steps

### Test 1: Test log rotation by size

1. Set a small size limit for testing
2. Generate many log entries
3. Verify new file is created when limit reached
4. Verify old file is handled correctly

### Test 2: Test log rotation by time

1. Wait for a new day (or change system date)
2. Generate log entries
3. Verify new file is created
4. Verify old file is preserved

### Test 3: Test automatic cleanup

1. Create old log files (manually or by changing date)
2. Start the application
3. Verify old logs are deleted
4. Verify only recent logs remain

### Test 4: Test retention configuration

1. Go to Settings
2. Change log retention period
3. Save
4. Verify the setting is applied
5. Verify cleanup uses new retention

### Test 5: Test maximum storage

1. Set a small maximum storage
2. Generate many logs
3. Verify oldest are deleted when limit reached
4. Verify total stays within limit

### Test 6: Test manual cleanup

1. Go to error logs
2. Click "Clear Old Logs"
3. Verify old logs are deleted
4. Verify space freed is shown

### Test 7: Test log file naming

1. Generate logs over several days
2. Examine the log folder
3. Verify naming is clear
4. Verify dates are in filenames

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Log rotation by size works
- [ ] Log rotation by time (daily) works
- [ ] Automatic cleanup of old logs works
- [ ] Log retention is configurable
- [ ] Maximum log storage is enforced
- [ ] Manual log cleanup is available
- [ ] Log files have clear names with dates
- [ ] Logs are stored in dedicated folder
- [ ] Cleanup happens automatically on startup
- [ ] Works on Windows, macOS, and Linux
- [ ] Log management doesn't impact performance
- [ ] No data loss during rotation