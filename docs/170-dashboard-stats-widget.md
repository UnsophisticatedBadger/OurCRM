# US-170: Dashboard Stats Widget

## User Story

**As an** agent  
**I want to** see a row of key business counts on the dashboard  
**So that** I can get an at-a-glance overview of my pipeline without navigating to each section

## Priority

**MVP:** Must Have

## Estimated Effort

**Size:** S — 1 day

## Dependencies

**Depends on:** US-133 (Home Dashboard)

**Feeds into:** US-020 (Contacts data), US-030 (Leads data), US-040 (Properties data), US-080 (Tasks data) — the widget is built now with zero/empty state; real counts are wired in when those slices land.

## Description

Replace the "Key Metrics — coming soon" placeholder with a `StatsWidget` showing four count tiles:

| Tile | Label | Initial value |
|------|-------|---------------|
| Total Contacts | "Contacts" | 0 |
| Active Leads | "Active Leads" | 0 |
| Properties | "Properties" | 0 |
| Tasks Due Today | "Due Today" | 0 |

The widget exposes a `refresh(counts: StatsData)` method so downstream slices can supply real numbers without touching the widget layout.

## Acceptance Criteria

- [x] Dashboard shows four stat tiles: Contacts, Active Leads, Properties, Due Today
- [x] Each tile displays a numeric count (0 when no data)
- [x] `StatsWidget.refresh(counts)` method exists and updates the displayed values
- [x] Widget layout is horizontal and clearly readable
