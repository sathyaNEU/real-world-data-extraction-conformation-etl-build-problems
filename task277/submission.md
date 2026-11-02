## Tags

**Domain:** Human Factors & Ergonomics (human reliability assessment: the human error probability per pick at a contract-logistics fulfilment site, carried to the order lines a client's plan creates).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**No: the Venlo site will not hold Siersma's 99.80 per cent pick accuracy in February or March 2027; expect about 100 order lines to fail pack-out verification in February and 110 in March, 99.7 per cent in both months.**
From February the Daily range sits in inners of four while its store lines keep their sixes and eighteens, so about two thirds of Daily retail lines become picks of whole inners plus loose units, which failed at 1.049 per cent through the record against 0.061 per cent for whole-inner picks. Not the record's rate by channel and range, which keeps the target only by carrying last year's mix of picks inside each category. Not the opened-inner rate on the Daily lines, which keeps it by blending that pick with loose picks below one inner, which fail at 0.111 per cent.

## 2. Critical Components

1. 2026 failure rate by the pick a line calls for: whole inners **0.061** per cent, loose units below one inner **0.111** per cent, whole inners plus loose units **1.049** per cent.
2. February 2027: **100** failing lines of **31,460** planned, **99.7** per cent.
3. March 2027: **110** failing lines of **35,170** planned, **99.7** per cent.

## 3. Step-by-Step Solution

1. Put wms_pick_confirmations_2026-01-01_2026-06-12.csv (local time) and wms_pick_confirmations_2026-06-15_2026-12-31.parquet (UTC) into one row per order line on its Amsterdam pick date, confirmations summed and lines confirmed at zero left out (Schedule 3, pick accuracy), and marked a line failing where packout_exceptions_2026.csv records SHORT, OVER or WRONG_ITEM against its SIE order reference and line: every month of the record is above target.
2. Read each line's inner in force on its pick date from siersma_item_master_2027-01-04.xlsx and classed the line by what its quantity asks of the picker: a whole number of inners, loose units below one inner, or whole inners plus loose units; their 2026 failure rates are 0.061, 0.111 and 1.049 per cent (109 of 177,273, 245 of 221,100 and 172 of 16,393 lines).
3. Took the Daily range's configuration for February and March from siersma_pcn_2026-11_daily_range.pdf and the item master's configuration dated from the first receipt in the new pack (inners of four, the old pack sold through by the end of January), every other article's unchanged.
4. Built each month's forward lines from siersma_volume_plan_q1_2027.xlsx (lines per range and channel; article mix and order sizes as the same month of 2026), classed every same-month 2026 line again under the 2027 inners, and carried each planned line at its class's rate: February 100 failing lines of 31,460, March 110 of 35,170, 99.7 per cent in both, below the 99.80 per cent target.
5. Matched siersma_store_claims_2026.csv to dispatch_deliveries_2026.csv by delivery note or store PO, kept accepted claims for Tekort, Teveel and Verkeerd artikel on 2026 deliveries, counted each claimed line once across its EDI and portal rows, converted portal quantities entered before the portal's July release break (offline 11 to 19 July) at the article's store order unit, and counted a missing-cage claim at the units its SSCC carried (dispatch_colli_2026-01_2026-06.csv before the cut-over, the new WMS's container field after it).
6. The site does not hold the target in either month.

## 4. Deliverable Answers

### venlo_accuracy_forecast_feb_mar_2027.xlsx

1. February 2027: 100 failing order lines, 99.7 per cent, target not held.
2. March 2027: 110 failing order lines, 99.7 per cent, target not held.
3. Accepted store claims for short, over or wrong articles on 2026 retail deliveries, units, by quarter of delivery:
   - Ravelijn Drogist: Q1 469, Q2 518, Q3 585, Q4 580
   - Hooghuys Drogisterij: Q1 347, Q2 359, Q3 488, Q4 598
   - Vlietmarkt Supermarkten: Q1 347, Q2 279, Q3 250, Q4 231
   - Independent drugstores: Q1 542, Q2 390, Q3 631, Q4 437

### siersma_pick_accuracy_q1_2027.png

1. Each month's accuracy through the record, the February and March 2027 forecasts at 99.7 per cent, and the 99.80 per cent target line.
