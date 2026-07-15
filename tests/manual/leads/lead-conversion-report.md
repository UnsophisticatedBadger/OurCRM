# Lead Conversion Report — Manual Tests

**Story:** [#95 — Lead Conversion Report](../../docs/95-lead-conversion-report.md)

## Report shows correct totals and conversion rate

1. Open OurCRM and navigate to **Leads → Conversion Report**
2. Confirm the default period is **This Month**
3. Verify total leads, converted count, and conversion rate match seeded or manually created leads

## Date range filter recalculates the report

1. Switch the period preset to **Last Month**
2. Confirm summary totals and the source table update
3. Choose **Custom**, set a narrower date range, and confirm only leads created in that range are counted

## Conversion rate by source is shown

1. Ensure leads from at least two sources exist in the selected period
2. Verify the source table lists each source with its own conversion rate

## Period comparison

1. Enable **Compare to previous period**
2. Confirm the comparison panel shows totals for the immediately preceding period of equal length

## Export to CSV

1. Click **Export to CSV** and save the file
2. Open the CSV and verify summary metrics, source rows, and trend buckets are present

## Export to PDF

1. Click **Export to PDF** and save the file
2. Open the PDF and verify summary text and the trend chart image are included
