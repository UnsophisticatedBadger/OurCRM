# US-175: Dashboard Quick Actions Navigation

## User Story

**As an** agent  
**I want** the Quick Actions buttons on the dashboard to navigate to the correct section  
**So that** I can jump directly to Contacts, Leads, Properties, or Tasks with one click

## Priority

**MVP:** Must Have

**Rationale:** The quick action buttons exist visually but do nothing when clicked. Without navigation wiring they are decoration, not functionality.

## Estimated Effort

**Size:** XS — 0.5 days

## Dependencies

**Depends on:** US-133 (Home Dashboard), US-016 (Navigate Between Sections)

## Description

Wire each button in `QuickActionsWidget` to call `navigate_to()` on the main window for the corresponding section:

| Button | Section |
|--------|---------|
| New Contact | Contacts |
| New Lead | Leads |
| New Property | Properties |
| New Task | Calendar (until a dedicated Tasks section exists) |

The `DashboardPage` must receive a callback or signal so it can trigger navigation without importing `MainWindow` (slice isolation rule).

## Acceptance Criteria

- [x] "New Contact" button navigates to the Contacts section
- [x] "New Lead" button navigates to the Leads section
- [x] "New Property" button navigates to the Properties section
- [x] "New Task" button navigates to the Calendar section
- [x] Navigation is triggered via callback/signal (no direct import of MainWindow from DashboardPage)
