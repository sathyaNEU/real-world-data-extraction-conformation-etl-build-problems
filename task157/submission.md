## Tags

**Domain:** Product Analytics (retention, cohort and lifetime value modeling: a ride-hail platform's supply-side driver cohorts, last winter's recruits read as a returning cohort whose resurrection is under way at the forecast date).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Fund the winter guarantee account with $1,650,000 at go-live on Monday 4 January: we expect 4,700 drivers to complete 40 trips by Sunday 31 January.**
About 1,100 of last winter's drivers, most of them recruits of the winter 2026 campaign who stopped driving in March and April, were back on the road by 3 January, and every earlier winter brought back about 1.1 drivers in January for each one back in November and December, so about 1,200 more are due inside the window and last winter's drivers make up about 2,000 of the 4,700. Not December's roster with the drivers away priced at last January's return rate, which treats last winter's drivers as a pool whose return rate moves with who sits in it: on last winter's drivers alone that rate over-predicted January 2026's returns, because the 2025 rental programme's drivers sat in the pool and never came back. Not one ratio of January to November and December returns over every driver back after a break, which mixes in occasional drivers who keep no seasonal timing. Not the drivers already back priced by their December trips, which under-predicted last year's back-by-December drivers' qualification.

## 2. Critical Components

1. About **1,100** of last winter's drivers (a trip from January to March 2026, none from May to October 2026) were back on the road by 3 January 2027.
2. Each of the 2024, 2025 and 2026 winters brought back about **1.1** drivers in January for every one back in November and December.
3. About **1,200** more of last winter's drivers are due back inside the window.
4. Last winter's drivers make up about **2,000** of the 4,700 drivers expected to qualify.

## 3. Step-by-Step Solution

1. Stacked dispatch_legacy_driver_months_2021-05_2024-07.csv (legacy driver numbers through dispatch_migration_driver_crosswalk.csv) with driver_activity_monthly_2024-07_2027-01.csv into completed trips by driver and month; last year's qualifiers are the accounts paid in winter_guarantee_2026_payout_run.csv and by the late credits in guarantee_payout_adjustments_2025-2026.csv, less the fraud recoveries.
2. Took each winter's drivers as those with a trip from January to March and none from May to October: 1,087 of last winter's had a trip in November or December 2026.
3. Over the 2024, 2025 and 2026 winters, January returns ran 1.086 times the November and December returns; at the 2025 and 2026 funding dates this ratio put January's returns within 2 per cent, where the previous January's share on the drivers still away missed by 14 and 16 per cent.
4. Priced December 2026's roster without last winter's drivers at the share of each December-trip band of December 2025's roster that the 2026 guarantee paid (about 2,700 drivers), last winter's drivers back by 3 January at the 93 per cent of 2026's back-by-December drivers it paid, and the 1,180 due back at the 82 per cent of January 2026's returners it paid.
5. Added the 26 drivers who came back after other breaks and qualified in January 2026, and the 195 accounts approved in the 90 days to 3 January without a first trip (onboarding_applications_2025-06-02_2027-01-03.csv; an approval lapses after 90 days) at the 14 of 174 accounts approved in the 90 days to 4 January 2026 with no first trip by the end of that day that the 2026 guarantee paid (the 9 that first drove on 1 to 4 January are not among them): 4,700 drivers expected to qualify, $1,650,000 at $350 each to the nearest $50,000 (guarantee_account_funding_2026-12-30.eml).
6. For each guarantee, a returned payout that guarantee_payout_events_2025-2026.csv shows sent again and settled reached its driver; only payouts whose last event is a return never did. Recoveries go to the guarantee of the payout they reverse, the 2025 run read in cents and people through merged_into in driver_accounts_2027-01-03.csv (winter_guarantee_payout_notes.docx).
7. For the pipeline, counted people by screening candidate in background_check_orders_2025-06_2027-01.csv, each in the month (Central time) of their first order, which is placed at first submission while the app's submitted time is the latest resubmission (onboarding_pipeline_counts.docx).

## 4. Deliverable Answers

### guarantee_fund_jan2027.xlsx

1. Fund at go-live, to the nearest $50,000: $1,650,000.
2. Drivers expected to qualify, to the nearest 100: 4,700.
3. 2025 guarantee: $12,950 never reached a driver; net cost $889,350; 2,541 drivers paid.
4. 2026 guarantee: $16,100 never reached a driver; net cost $1,038,450; 2,966 drivers paid.
5. Onboarding pipeline by month of first application, whole people:
   - June 2026: 446 applied, 313 approved, 263 with a first trip by 3 January 2027
   - July 2026: 448 applied, 322 approved, 274 with a first trip by 3 January 2027
   - August 2026: 500 applied, 350 approved, 294 with a first trip by 3 January 2027
   - September 2026: 423 applied, 311 approved, 255 with a first trip by 3 January 2027
   - October 2026: 481 applied, 338 approved, 286 with a first trip by 3 January 2027

### guarantee_fund_jan2027.pptx

6. Slide 1 states the fund, $1,650,000 at go-live, with the 4,700 drivers expected to qualify.
7. Slide 2 charts each guarantee from main run to net cost:
   - 2025: main run $900,900, later runs $5,950, never reached a driver $12,950, recovered $4,550, net cost $889,350
   - 2026: main run $1,053,500, later runs $7,350, never reached a driver $16,100, recovered $6,300, net cost $1,038,450
