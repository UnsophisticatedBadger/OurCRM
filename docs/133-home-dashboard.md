# US-133: Home Dashboard

## User Story

**As an** agent  
**I want to** see a dashboard when I open the app  
**So that** I can quickly see what's important today and get an overview of my business

## Priority

**MVP:** Should Have

**Rationale:** A dashboard provides a quick overview of the agent's day and business performance. Instead of navigating to multiple sections, agents can see today's schedule, overdue tasks, recent activity, and key metrics at a glance. This improves productivity and helps agents prioritize their work.

## Estimated Effort

**Size:** Medium (M) - 3-5 days

**Breakdown:**
- 2 hours: Design dashboard layout
- 3 hours: Create dashboard widgets
- 2 hours: Implement today's schedule widget
- 2 hours: Implement recent activity feed
- 2 hours: Implement key metrics widget
- 2 hours: Implement overdue tasks widget
- 2 hours: Test dashboard
- 2 hours: Test on all platforms

## Dependencies

**Depends on:** US-077 (View Calendar), US-081 (View Task List), US-085 (View Overdue Tasks)

**Blocks:** None

## Description

The home dashboard should be the default view when opening OurCRM. It should include:
1. **Today's Schedule**: Showings, appointments, and events for today
2. **Overdue Tasks**: List of tasks past due date
3. **Key Metrics**: Lead count, conversion rate, active listings, etc.
4. **Recent Activity**: Recent changes across contacts, leads, properties
5. **Quick Actions**: Buttons for common actions (new contact, new lead, etc.)

The dashboard should be customizable (widgets can be rearranged or hidden) but for MVP, a fixed layout is acceptable.

## BDD Scenarios

### Scenario 1: Dashboard is default view

Given I open OurCRM And I am logged in When the application loads Then I should see the dashboard And it should be the default view


### Scenario 2: Today's schedule widget

Given I have events scheduled for today When I view the dashboard Then I should see today's schedule Including: - Showings - Appointments - Meetings - With times and locations


### Scenario 3: Overdue tasks widget

Given I have overdue tasks When I view the dashboard Then I should see the overdue tasks And they should be prominently displayed And I can click to view or complete them


### Scenario 4: Key metrics widget

Given I have data in the system When I view the dashboard Then I should see key metrics:

Total leads
Active listings
Conversion rate
Tasks due today And the numbers should be accurate

### Scenario 5: Recent activity feed

Given there has been recent activity When I view the dashboard Then I should see a feed of recent activities:

New leads
Updated contacts
Completed tasks
With timestamps

### Scenario 6: Quick actions widget

Given I am viewing the dashboard When I look at quick actions Then I should see buttons for:

New Contact
New Lead
New Property
New Task And clicking them should open the appropriate form

### Scenario 7: Click to navigate

Given I am viewing the dashboard When I click on a widget item (e.g., a task) Then I should be taken to the relevant section And the specific item should be selected


### Scenario 8: Dashboard loads quickly

Given I have a lot of data When I open the dashboard Then it should load in under 3 seconds And all widgets should display correctly


## Manual Testing Steps

### Test 1: Dashboard is default view

1. Log in to OurCRM
2. Verify the dashboard appears
3. Verify it's the first thing you see
4. Verify navigation shows "Dashboard" as selected

### Test 2: Test today's schedule

1. Create some events for today
2. View the dashboard
3. Verify they appear in Today's Schedule
4. Verify times and locations are shown
5. Click on an event
6. Verify it opens the event details

### Test 3: Test overdue tasks

1. Create some overdue tasks
2. View the dashboard
3. Verify they appear in Overdue Tasks
4. Verify they're prominently displayed
5. Click on a task
6. Verify it opens the task

### Test 4: Test key metrics

1. Create leads, properties, etc.
2. View the dashboard
3. Verify the metrics are shown
4. Verify the numbers are accurate
5. Manually count to verify

### Test 5: Test recent activity

1. Perform various actions (create lead, update contact, etc.)
2. View the dashboard
3. Verify the activities appear
4. Verify timestamps are shown
5. Verify it's in chronological order

### Test 6: Test quick actions

1. View the dashboard
2. Click "New Contact"
3. Verify the form opens
4. Test other quick actions
5. Verify they all work

### Test 7: Test navigation from dashboard

1. Click on a task in the widget
2. Verify it navigates to Tasks
3. Verify the task is selected
4. Test with other items

### Test 8: Test performance

1. Create lots of data
2. Open the dashboard
3. Measure load time
4. Verify it's under 3 seconds
5. Verify all widgets load

### Test 9: Test on all platforms

1. Test on Windows
2. Verify it works
3. Test on macOS
4. Verify it works
5. Test on Linux
6. Verify it works
7. Document any platform-specific issues

## Acceptance Criteria

- [ ] Dashboard is the default view after login
- [ ] Today's Schedule widget shows today's events
- [ ] Overdue Tasks widget shows overdue tasks
- [ ] Key Metrics widget shows important numbers
- [ ] Recent Activity widget shows recent changes
- [ ] Quick Actions widget provides common actions
- [ ] Clicking items navigates to relevant sections
- [ ] Dashboard loads in under 3 seconds
- [ ] All metrics are accurate
- [ ] All data is up-to-date
- [ ] Works on Windows, macOS, and Linux
- [ ] Dashboard is visually appealing and organized
- [ ] Widgets are clearly labeled