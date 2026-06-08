# US-062: Quick Actions Menu

## User Story

**As an** agent  
**I want to** access quick actions (create new contact, lead, property, etc.) from the global search  
**So that** I can perform common tasks quickly without navigating through menus

## Priority

**MVP:** Should Have (could be deferred to post-MVP)

**Rationale:** Quick actions improve workflow efficiency. Instead of navigating to a section and clicking "New", agents can press Ctrl+K and type "new contact" to create one immediately. This is a productivity booster but not essential for MVP. Can be deferred to v0.2 if needed.

## Estimated Effort

**Size:** Small (S) - 1 day

**Breakdown:**
- 1 hour: Design quick actions UI
- 1 hour: Implement action commands (new contact, new lead, etc.)
- 1 hour: Add action recognition in global search
- 1 hour: Create action handlers
- 1 hour: Add keyboard navigation for actions
- 1 hour: Test quick actions
- 1 hour: Test on all platforms

## Dependencies

**Depends on:** US-060 (Search Contacts Globally), US-061 (Search Across All Sections)

**Blocks:** US-063 (Recent Searches)

## Description

The global search interface should also recognize action commands. When a user types something like "new contact" or "create lead", the system should show quick action options that can be executed immediately. This allows agents to perform common tasks without navigating through the UI.

Quick actions include:
- New Contact
- New Lead
- New Property
- New Transaction
- New Showing
- New Note
- Open Settings
- Check for Updates

## BDD Scenarios

### Scenario 1: Show quick actions

```
Given the global search is open
  And the search box is empty or has no matching results
When I type "new" or "create"
Then I should see quick action suggestions:
  - New Contact
  - New Lead
  - New Property
  - New Transaction
```

### Scenario 2: Execute quick action

```
Given the global search is open
  And I see "New Contact" as a quick action
When I select it (arrow keys + Enter, or click)
Then the new contact form should open
  And the global search should close
```

### Scenario 3: Quick actions appear with search results

```
Given the global search is open
  And I type "jo"
When results appear
Then quick actions should also appear:
  - New Contact
  - New Lead
  And they should be separated from search results
```

### Scenario 4: Keyboard navigation for actions

```
Given the global search is open
  And I see quick actions and search results
When I press the down arrow
Then the first quick action should be highlighted
  And subsequent arrows should move through actions
  And results should be navigable separately
```

### Scenario 5: Quick action: Open Settings

```
Given the global search is open
When I type "settings" or "preferences"
Then I should see "Open Settings" as a quick action
  And selecting it opens the Settings window
```

### Scenario 6: Quick action: Check for Updates

```
Given the global search is open
When I type "update" or "check for updates"
Then I should see "Check for Updates" as a quick action
  And selecting it runs the update check
```

### Scenario 7: Quick actions for navigation

```
Given the global search is open
When I type "contacts" or "leads" or "properties"
Then I should see "Go to Contacts" or similar navigation actions
  And selecting them navigates to that section
```

### Scenario 8: Fuzzy matching for actions

```
Given the global search is open
When I type "new cont" (partial)
Then "New Contact" should appear as a quick action
  And it should be matched even with partial input
```

## Manual Testing Steps

### Test 1: Show quick actions

1. Open global search (Ctrl+K)
2. Type "new"
3. Verify quick actions appear
4. Verify they include New Contact, New Lead, etc.

### Test 2: Execute quick action

1. Open global search
2. Type "new contact"
3. Select "New Contact"
4. Verify the new contact form opens
5. Verify the global search closes

### Test 3: Test with search results

1. Open global search
2. Type something that has both results and actions
3. Verify both are shown
4. Verify they're separated visually

### Test 4: Test keyboard navigation

1. Open global search
2. Type to see actions and results
3. Navigate with arrow keys
4. Verify you can move between actions and results
5. Press Enter on an action
6. Verify it executes

### Test 5: Test settings action

1. Open global search
2. Type "settings"
3. Verify "Open Settings" appears
4. Select it
5. Verify Settings opens

### Test 6: Test update action

1. Open global search
2. Type "update"
3. Verify "Check for Updates" appears
4. Select it
5. Verify the update check runs

### Test 7: Test navigation actions

1. Open global search
2. Type "contacts"
3. Verify "Go to Contacts" appears
4. Select it
5. Verify it navigates to Contacts

### Test 8: Test fuzzy matching

1. Open global search
2. Type "new cont"
3. Verify "New Contact" appears
4. Test with various partial inputs
5. Verify fuzzy matching works

### Test 9: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Quick actions appear in global search
- [ ] Common actions are available (new contact, lead, property, etc.)
- [ ] Actions can be executed with keyboard or mouse
- [ ] Actions and results are visually separated
- [ ] Keyboard navigation works for actions
- [ ] Fuzzy matching works for action names
- [ ] Settings action works
- [ ] Update check action works
- [ ] Navigation actions work
- [ ] Actions are discoverable
- [ ] Works on Windows, macOS, and Linux
- [ ] Actions are fast and responsive
- [ ] UI is intuitive