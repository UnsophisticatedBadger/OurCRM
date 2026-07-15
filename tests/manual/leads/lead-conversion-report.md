# Lead Conversion Report — Manual Tests

**Story:** [#95 — Lead Conversion Report](../../../docs/95-lead-conversion-report.md)

## Prerequisites

The conversion report reads from an **in-memory** `LeadRepository`. A fresh `uv run ourcrm` launch starts with **no leads**; the **Pipeline** tab still shows *Lead pipeline — coming soon*. Persistent lead CRUD and session-to-session data depend on [#67 — Mark Lead as Converted](https://github.com/UnsophisticatedBadger/OurCRM/issues/67) and [#69 — Track Conversion Rate](https://github.com/UnsophisticatedBadger/OurCRM/issues/69).

Until the pipeline is integrated, use this split:

| Check type | How to verify |
|------------|---------------|
| Report UI, filters, comparison layout, export dialogs | Manual steps below marked **UI only** — no lead data required |
| Totals, rates, source rows, trend values | **Pending #67/#69** — run `uv run pytest -m story_95` (BDD fixtures seed leads automatically) |

---

## Report shows correct totals and conversion rate

**Pending #67/#69** — requires leads in the repository.

1. Open OurCRM and navigate to **Leads → Conversion Report**
2. Confirm the default period is **This Month**
3. ~~Verify total leads, converted count, and conversion rate match seeded or manually created leads~~
4. **Interim:** confirm the summary shows `0` totals on a fresh launch; for populated data, run `uv run pytest -m story_95`

## Date range filter recalculates the report

**UI only** (empty state) + **Pending #67/#69** (populated totals)

1. Switch the period preset to **Last Month**
2. Confirm summary labels and the source table refresh (zeros on a fresh launch)
3. Choose **Custom**, set a narrower date range, and confirm the report recalculates without error
4. **After #67/#69:** repeat with real leads and confirm only leads *created* in the custom range count toward total leads

## Conversion rate by source is shown

**Pending #67/#69** — requires leads from at least two sources in the selected period.

1. Ensure leads from at least two sources exist in the selected period
2. Verify the source table lists each source with its own conversion rate
3. **Interim:** on a fresh launch, confirm the source table is empty and the report does not error

## Period comparison

**UI only**

1. Enable **Compare to previous period**
2. Confirm the previous-period column appears beside the current period
3. Confirm both columns show summary fields for their respective date ranges (zeros on a fresh launch)

## Export to CSV

**UI only** (empty report) — export file structure can be verified without lead data.

1. Click **Export to CSV** and save the file
2. Open the CSV and verify it contains period headers, column labels, and trend bucket rows (values may be zero)

## Export to PDF

**UI only** (empty report) — PDF layout and chart placeholder can be verified without lead data.

1. Click **Export to PDF** and save the file
2. Open the PDF and verify it contains summary text and a trend chart section (chart may show an empty axis when no leads exist)
