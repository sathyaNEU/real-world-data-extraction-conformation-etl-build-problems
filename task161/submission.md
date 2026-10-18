## Tags

**Domain:** Urban & Regional Science (forecasting: an import 3PL's pallet positions beside the San Pedro Bay ports for January to June 2027, each account's bought-ahead stock netted against its own forecast shipments at the share its own earlier duty rushes burned, against six 4,000-position overflow blocks).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**We should take 2 of the six 4,000-position overflow blocks at Tamarind Avenue Logistics Park for January to June 2027, $2,200,000 for the term.**
Netted account by account against each account's own forecast shipments, the stock runs 7,342 to 9,294 positions above our 40,000 rack positions every month, so the second block would hold 96.7% of its 24,000 position-months against the space policy's 75% and the third 9.8%. Not fading the book's excess at the 0.97-month half-life the earlier rushes showed, which leaves overflow only in January (block 1 used 17%) and takes no block: five seasonal accounts that bought for their whole 2027 season hold 17,541 of the 20,063 pallets of excess and ship little before summer. Not burning the book's excess at the book's share of its shipments (0.125 of each pallet shipped), which takes no block, nor each account's own monthly fall from the earlier rushes (one block), nor holding the whole excess through June (three blocks).

## 2. Critical Components

1. Pallets on hand at the close of 6 December for the accounts under contract: **50,449**.
2. Pallets over normal stock at 31 December: **20,063**, of which the five seasonal accounts hold **17,541**.
3. Pallets over normal stock still on hand at 30 June 2027: **10,123**.
4. Block uses over the term: block 1 **100.0%**, block 2 **96.7%**, block 3 **9.8%**.

## 3. Step-by-Step Solution

1. Stacked wms1_inv_daily_20190401-20220930.txt to the close of 11 September 2022 (Sundays carrying Saturday's close, legacy codes mapped through client_master_2026-12.xlsx, ROSALESB and ROSALESK as PD2063) with wms_inventory_nightly_20220913_20261207.csv summed over sites (each run holding the close of the day before it, per wms_export_dictionary_v3.pdf) and wms_outbound_daily_20220912_20261206.csv: 50,449 pallets on hand at the close of 6 December.
2. Set each account's normal stock at mid-month as its cover times the mean of that and the next month's shipments (actual, then forecast), interpolated by day, the cover being its median, over its months from July 2023 clear of each duty step's month, the three months before it and the five after, of pallets on hand over the mean of that and the next month's shipments.
3. For each duty step in yv_client_advisories_2019-2026.pdf (1 September 2019, 5 April 2025, 7 August 2025) where an account's excess over normal stock, its mean over the seven days before the step, was at least 12% of normal stock, fitted the fall in that excess against cumulative shipments from the step (a least-squares slope with an intercept) until the excess fell under a quarter of its size or the next advisory, keeping fits of 15 days or more: each account's burn share is the shipment-weighted mean of its episodes, 0.062 to 0.238.
4. Forecast each account's shipments for December 2026 to July 2027 as the same month a year earlier times its shipments from December 2025 to November 2026 over the twelve months before, spread over each month's working days with a Saturday at 0.40 of a weekday (the book's own ratio) and Sundays, Christmas Eve, Christmas Day, New Year's Day and Memorial Day closed.
5. Projected each account's close of 31 December as the close of 6 December plus the pallets due in dec2026_inbound_booking_tracker.xlsx (box-only notices at the account's own pallets per box over the last 90 days, per the tracker) less the rest of December's forecast shipments: 20,063 pallets over normal stock, 17,541 of them with the five seasonal accounts.
6. Burned each account's excess day by day at its burn share of its forecast shipments until it was gone, added its normal stock and took the mean of each day's close by month (space policy 3.1): overflow above 40,000 of 9,294, 8,203, 8,520, 8,337, 7,878 and 7,342 positions from January to June, with 10,123 pallets of excess left at 30 June.
7. Ran the block test of space_planning_policy_rev4.pdf section 4.2: blocks 1 and 2 hold 100.0% and 96.7% of their 24,000 position-months and block 3 9.8%, so we take 2 blocks, $2,200,000 at the $1,100,000 per block in ridley-ames_bldg-b_overflow_blocks_2026-11-19.pdf.

## 4. Deliverable Answers

### overflow_blocks_h1_2027.xlsx

1. The call on the Blocks sheet: take 2 of the 6 blocks (B-1 and B-2), $2,200,000 for the term; block uses 100.0%, 96.7% and 9.8%.
2. Pallets we held outside our racks at the close of 6 December, by building:
   - CAR1 (Del Amo, Carson): 1,815
   - RDZ1 (Alondra, Rancho Dominguez): 1,589
   - WIL1 (Anaheim Street, Wilmington): 1,042
   - CMP1 (Artesia, Compton): 776
3. TEU of the import containers whose freight reached us from the two ports, and that TEU as a share of the two ports' loaded import TEU, by month of 2026:
   - January: 1,896 TEU, 0.222%
   - February: 2,227 TEU, 0.298%
   - March: 2,460 TEU, 0.290%
   - April: 2,406 TEU, 0.285%
   - May: 2,499 TEU, 0.279%
   - June: 2,653 TEU, 0.289%
   - July: 2,829 TEU, 0.291%
   - August: 3,039 TEU, 0.311%
   - September: 3,434 TEU, 0.346%
   - October: 3,356 TEU, 0.328%

### port_share_2026.pdf

1. One-page bar chart of the ten monthly shares, January to October 2026, each bar labelled with its month's TEU and share.
