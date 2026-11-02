## Tags

**Domain:** General Statistics & Data Science, missing data, censoring and measurement error (retail price integrity).
**Analytical objective:** Data Quality Monitoring & Alerting.

## 1. Final Recommendation

**Put Spryfield (102), Lower Sackville (107), Antigonish (203), Bridgewater (205) and Yarmouth (206) on Price Watch for the first quarter of 2027.**
Their fourth-quarter price accuracy is 98.4%, 98.6%, 98.3%, 98.7% and 97.8% against the 99.0% line, and Cole Harbour (106) is the nearest store to stay off at 99.4%. Not the weekly random price audits, which check labels at random moments and put every store at 99.9% or more. Not the Thursday checks' share of labels still at the old price, which also puts Cole Harbour on.

## 2. Critical Components

1. Spryfield (102) price accuracy for Q4 2026 is **98.4%**
2. Lower Sackville (107) price accuracy for Q4 2026 is **98.6%**
3. Antigonish (203) price accuracy for Q4 2026 is **98.3%**
4. Bridgewater (205) price accuracy for Q4 2026 is **98.7%**
5. Yarmouth (206) price accuracy for Q4 2026 is **97.8%**
6. Cole Harbour (106), the nearest store above the line, is at **99.4%**

## 3. Step-by-Step Solution

1. Totalled each store's item scans from 1 October to 31 December 2026 in pos_hourly_item_scans_2026Q4.csv.
2. For each changeover Thursday took each store's completed PCB batch (print time read in local time, label count) from label_printer_fleet_jobs_2026-10-01_2026-12-31.jsonl and the units its price-changed items scanned that Thursday from price_change_item_movement_2026Q4.csv.
3. Read the hanging pace from thursday_changeover_checks_Q4-2026.xlsx: the share of checked labels still at the old price falls from all of them at the print to none once the batch is up, at one pace for every store.
4. Spread each changeover's changed-item units over that Thursday's hours as the store's own hourly scans, and counted as off the label the units scanned before the batch printed and, while it was going up, the share of its labels not yet hung.
5. Added stray labels at the share price_audit_results_2026Q4.csv finds outside changeovers, and took price accuracy as one minus the off-label scans over the item scans (PI-2 s.3.1): Spryfield (102), Lower Sackville (107), Antigonish (203), Bridgewater (205) and Yarmouth (206) below 99.0%, Cole Harbour (106) nearest above at 99.4% (s.4.1).
6. Scanner Code payouts: SC overrides in pos_price_overrides_2026Q4.csv (original less override price, UTC converted to local, in the quarter) plus Scanner Code refunds in service_desk_adjustments_Q4_2026.xlsx, a desk refund dropped only when it repeats a register payout of the same amount on the same receipt line and kept when it pays the rest of the Code remedy (s.5.1).
7. Flyer prices: every advertised UPC of flyer_ad_plan_wk40-wk53_2026.csv (an assorted line's varieties matched by brand, product and size among the week's AD START items) against the REVISED sheet of weekly_price_change_releases_2026Q4.xlsx in each zone, per unit for multi-buys, with the price paid above the flyer times that zone's units in flyer_item_weekly_units_2026Q4.csv.
8. Put the five stores below 99.0% on Price Watch.

## 4. Deliverable Answers

### price_watch_2027q1.xlsx

1. Price Watch for Q1 2027, with each Price Watch store's Q4 2026 price accuracy:
   - 101 Quinpool Road: stays off
   - 102 Spryfield: Price Watch, 98.4%
   - 103 Clayton Park: stays off
   - 104 Bedford Place: stays off
   - 105 Dartmouth - Portland St: stays off
   - 106 Cole Harbour: stays off
   - 107 Lower Sackville: Price Watch, 98.6%
   - 201 Truro (Prince St): stays off
   - 202 New Glasgow: stays off
   - 203 Antigonish: Price Watch, 98.3%
   - 204 Kentville: stays off
   - 205 Bridgewater: Price Watch, 98.7%
   - 206 Yarmouth: Price Watch, 97.8%
   - 207 Amherst: stays off
2. Dollars paid out under the Scanner Price Accuracy Code in Q4 2026, to the nearest dollar:
   - 101 Quinpool Road: $13
   - 102 Spryfield: $760
   - 103 Clayton Park: $11
   - 104 Bedford Place: $25
   - 105 Dartmouth - Portland St: $3
   - 106 Cole Harbour: $348
   - 107 Lower Sackville: $864
   - 201 Truro (Prince St): $6
   - 202 New Glasgow: $112
   - 203 Antigonish: $524
   - 204 Kentville: $4
   - 205 Bridgewater: $527
   - 206 Yarmouth: $814
   - 207 Amherst: $61
3. Flyer weeks that started in the quarter: advertised UPCs that rang up at a price other than the flyer price, and dollars customers paid above the flyer price that week:
   - Week of 1 October 2026: 5 UPCs, $314
   - Week of 8 October 2026: 8 UPCs, $4,427
   - Week of 15 October 2026: 1 UPCs, $19
   - Week of 22 October 2026: 3 UPCs, $163
   - Week of 29 October 2026: 6 UPCs, $99
   - Week of 5 November 2026: 1 UPCs, $11
   - Week of 12 November 2026: 3 UPCs, $129
   - Week of 19 November 2026: 6 UPCs, $357
   - Week of 26 November 2026: 5 UPCs, $123
   - Week of 3 December 2026: 6 UPCs, $3,234
   - Week of 10 December 2026: 3 UPCs, $1,823
   - Week of 17 December 2026: 7 UPCs, $481
   - Week of 24 December 2026: 6 UPCs, $368
   - Week of 31 December 2026: 0 UPCs, $0

### price_accuracy_q4_2026.svg

1. Dot chart of every store's Q4 2026 price accuracy against the dashed 99.0% Price Watch line, the five Price Watch stores in orange with their accuracy labelled, the others in blue.
