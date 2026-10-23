## Tags

**Domain:** Economics & Econometrics (forecasting and forecast evaluation).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Put $13.75 million in the 2027 revenue certificate as the toll collected on the toll billed by mail to today's cash-lane users.** An in-state invoice unpaid at 60 days is collected when its plate next renews its two-year registration, so the in-state share is read on the held invoices whose registration on file has since expired: 94 per cent in-state and 60 per cent out-of-state. Not the share of invoices a year old, which counts in-state invoices still waiting on a renewal. Not the share across every toll-by-mail and violation invoice, which mixes in the violators.

## 2. Critical Components

1. Share of in-state toll billed by mail eventually collected: **94 per cent**.
2. Share of out-of-state toll billed by mail eventually collected: **60 per cent**.

## 3. Step-by-Step Solution

1. Took the overnight toll-by-mail invoices (invoice_type TOLL-BY-MAIL in tbm_invoices_2025-04_2026-10.csv) and applied each invoice's payments in tbm_payments_2025-04_2026-11.csv posted to 31 October 2026, net of reversals, toll first.
2. In-state, among invoices at least 61 days old, 61.0 per cent of the toll was paid within 60 days of issue.
3. For the in-state toll still unpaid at 60 days, joined dmv_registration_holds_2025-2026.csv: of the held invoices whose registration on file (reg_expires) had expired by 31 October 2026, 86.1 per cent of the toll was paid; invoices with no Division record were read on those a year old, as the agency had closed them.
4. Combined the two: 94 per cent of in-state toll is eventually collected; out-of-state, the invoices issued a year or more before 31 October 2026 collected 60 per cent.
5. Applied the shares to the 2027 toll billed by mail in aet_cutover_revenue_plan_2027.docx ($11,908,500 in-state, $4,292,700 out-of-state): $13.75 million, to the nearest $0.25 million.
6. For the violation tables, counted each express-lane vehicle read in both lanes within a second once, and dropped violation lines read 0.4 seconds or less behind a commercial posting in the same lane in marrowpass_commercial_postings_2026-01_2026-09.parquet (a trailer or towed car split off a MarrowPass truck), then counted crossings and summed toll by month of crossing.
7. For the out-of-state violation invoices, applied each agency settlement in tbm_payments_2025-04_2026-11.csv (no invoice number; its reference lists the invoices) oldest invoice first, toll before fees, and divided the toll collected on owed crossings by the toll owed, by quarter of issue.

## 4. Deliverable Answers

### aet_2027_toll_by_mail_forecast.xlsx

1. Toll collected in 2027 on the toll billed by mail to today's cash-lane users: $13.75 million.
2. Share eventually collected: in-state 94 per cent; out-of-state 60 per cent.
3. Violation crossings and toll owed, by month of crossing in 2026:
   - January: 15,003 crossings, $34,730.85 owed
   - February: 13,740 crossings, $31,764.50 owed
   - March: 15,530 crossings, $35,840.85 owed
   - April: 14,758 crossings, $34,341.75 owed
   - May: 15,332 crossings, $35,140.10 owed
   - June: 14,970 crossings, $34,115.05 owed
   - July: 15,285 crossings, $35,075.85 owed
   - August: 14,918 crossings, $34,673.90 owed
   - September: 14,368 crossings, $33,446.00 owed
4. Out-of-state violation invoices, share of toll owed collected by 31 October 2026, by quarter of issue:
   - April to June 2025: 44 per cent
   - July to September 2025: 48 per cent
   - October to December 2025: 41 per cent
   - January to March 2026: 40 per cent
