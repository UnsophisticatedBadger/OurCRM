# US-063: Recent Searches and Quick Access

## User Story

**As an** agent  
**I want to** see my recent searches and frequently accessed items  
**So that** I can quickly return to what I was working on

## Priority

**MVP:** Should Have (could be deferred to post-MVP)

**Rationale:** Recent searches and quick access improve workflow by surfacing what the agent was recently working on. While helpful, this is a convenience feature that can be deferred to v0.2 if needed. Agents can always search again if they don't have recent items.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design recent searches UI
- 1 hour: Track recent searches
- 1 hour: Display recent items in global search
- 1 hour: Implement recent items clearing
- 1 hour: Add quick access to recently viewed records
- 1 hour: Test recent searches
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-060 (Search Contacts Globally), US-061 (Search Across All Sections)

**Blocks:** None

## Description

The global search interface should show recent searches when opened with an empty query. This allows agents to quickly repeat searches or access recently viewed items. Recent searches are stored locally and can be cleared by the user.

The system should also track recently viewed contacts, leads, properties, and transactions, making them easily accessible. This helps agents return to their work quickly.

## BDD Scenarios

### Scenario 1: Show recent searches

```
Given I have performed several searches recently
When I open global search (Ctrl+K)
  And the search box is empty
Then I should see my recent searches listed
  And I can click one to re-run it
```

### Scenario 2: Track recent searches

```
Given the global search is open
When I perform a search
Then it should be added to my recent searches
  And the most recent should appear at the top
```

### Scenario 3: Limit recent searches

```
Given I have performed many searches
When I view recent searches
Then only the most recent 10-20 should be shown
  And older searches should be removed automatically
```

### Scenario 4: Clear recent searches

```
Given I am viewing recent searches
When I click "Clear Recent Searches"
Then all recent searches should be removed
  And the list should be empty
```

### Scenario 5: Recent items (contacts, properties, etc.)

```
Given I have recently viewed contacts, leads, and properties
When I open global search
  And the search box is empty
Then I should see my recently viewed items
  And I can click one to open it
```

### Scenario 6: Recent items are tracked

```
Given I open a contact's details
When I close and reopen global search
Then that contact should appear in my recent items
```

### Scenario 7: Click recent item to open

```
Given I see a recent contact in global search
When I click on it
Then the contact's details should open
  And the global search should close
```

### Scenario 8: Recent searches are private

```
Given I have recent searches saved
When they are stored
Then they should be stored locally only
  And not synced anywhere
  And not shared with anyone
```

## Manual Testing Steps

### Test 1: Show recent searches

1. Perform several searches
2. Open global search with empty query
3. Verify recent searches are shown
4. Verify they're in reverse chronological order
5. Click on one to re-run it

### Test 2: Test tracking

1. Perform a search
2. Open global search again
3. Verify the search is in the recent list
4. Perform another search
5. Verify the new one is at the top

### Test 3: Test limit

1. Perform many searches (20+)
2. Open global search
3. Verify only the most recent are shown
4. Verify older ones are removed

### Test 4: Test clearing

1. Have recent searches
2. Click "Clear Recent Searches"
3. Verify all are removed
4. Verify the list is empty

### Test 5: Test recent items

1. Open several contacts and properties
2. Open global search
3. Verify they appear in recent items
4. Verify they're in the order you viewed them

### Test 6: Test clicking recent item

1. Open global search
2. See a recent contact
3. Click on it
4. Verify the contact opens
5. Verify global search closes

### Test 7: Test privacy

1. Perform searches
2. Check the database or config files
3. Verify searches are stored locally
4. Verify they're not sent anywhere

### Test 8: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Recent searches are shown when global search opens with empty query
- [ ] Recent searches are tracked automatically
- [ ] Recent searches are limited to a reasonable number (10-20)
- [ ] Recent searches can be cleared
- [ ] Recently viewed items are shown
- [ ] Clicking a recent item opens it
- [ ] Recent searches are stored locally only
- [ ] Recent searches are private
- [ ] Works on Windows, macOS, and Linux
- [ ] Recent items are in reverse chronological order
- [ ] Performance is good
- [ ] UI is clean and non-intrusive