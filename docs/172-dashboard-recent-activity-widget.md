# US-172: Dashboard Recent Activity Widget

## User Story

**As an** agent  
**I want to** see a feed of recent changes across the app on the dashboard  
**So that** I can quickly catch up on what has changed since I last used OurCRM

## Priority

**MVP:** Must Have

## Estimated Effort

**Size:** S — 1 day

## Dependencies

**Depends on:** US-133 (Home Dashboard), US-080 (Create a Task), US-082 (Mark Task Complete), US-020 (Create a New Contact)

**Note:** The activity feed grows richer as more slices land. MVP scope covers tasks and contacts; leads and properties are added in their respective slices.

## Description

Replace the "Recent Activity — coming soon" placeholder with a `RecentActivityWidget` showing the last 10 activity events across tasks and contacts, newest first. Each entry shows a timestamp, action type (e.g. "Task completed", "Contact added"), and entity name. The widget refreshes automatically when the main window regains focus.

If no activity exists the widget shows "No recent activity."

## BDD Scenarios

### Scenario: Widget shows recently completed task

```
Given a task "Call back John" was completed today
And the dashboard is the active section
Then the Recent Activity widget shows "Task completed: Call back John"
```

### Scenario: Widget shows recently added contact

```
Given a contact "Jane Smith" was added today
And the dashboard is the active section
Then the Recent Activity widget shows "Contact added: Jane Smith"
```

### Scenario: Widget shows empty state with no activity

```
Given no tasks or contacts exist
And the dashboard is the active section
Then the Recent Activity widget shows "No recent activity"
```

## Acceptance Criteria

- [ ] Recent Activity widget shows last 10 events, newest first
- [ ] Each entry shows timestamp, action type, and entity name
- [ ] Covers: tasks created/completed, contacts created/edited
- [ ] Empty state shown when no activity exists
- [ ] Widget refreshes when the main window regains focus
