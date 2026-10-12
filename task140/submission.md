## Tags

**Domain:** General Statistics & Data Science (regression and model diagnostics: a dependent platform service's load specified on its two drivers and read forward at the guarantee it depends on, in a data-centre capacity plan).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**C-22 can guarantee 109,000 cores to batch training for the first quarter of 2027.**
That is the largest whole thousand the quarter's 726,624 reservable cores leave after the firm tenants' 577,000 and the platform services' 40,000, with cell-store reserved at its busiest hour as its own hourly use predicts it from its two drivers (2.9404 cores per machine in service, 0.20804 per batch core running) at 5,220 machines and the batch tier at the guarantee itself, so the guarantee and the cell-store reservation are solved together. Not 122,000, which carries cell-store forward on the line through its last four quarterly busiest hours and leaves out the storage load every added batch core brings; not 106,000, which adds that load once, at the 122,000 guarantee, instead of at the guarantee it is reserved under.

## 2. Critical Components

1. Reservable cores for 2027 Q1 are **726,624**.
2. The firm tenants' approved reservations total **577,000** cores (576,972), with search-api, pricing and reco-serve held to their frozen budgets.
3. cell-store's busiest-hour forecast at the guarantee is **38,000** cores (38,058); cell-ctl's is **2,000** (1,999).
4. The guarantee before the whole thousand is **109,492** cores.

## 3. Step-by-Step Solution

1. Took the 5,220 machines the hardware plan (revision of 11 December) has in service from 28 December at 96 cores and the capacity memo's overcommit of 1.45 (CS-3 2.1): 726,624 reservable cores.
2. Held each request in capacity_requests_2027Q1.csv to the whole cores its January 2027 MAD1 C-22 budget line (tech_budgets_2026_Q1-2027_freeze.xlsx, joined on the cost centre in tenant_directory.json) buys at EUR 7.42, the MAD1 reserved-core rate from 1 January 2027 (CS-3 3.2 and 3.3): search-api, pricing and reco-serve are held and the approvals total 576,972.
3. Forecast cell-ctl's busiest hour as the line through its four 2026 quarterly busiest hours in the monitoring export, one quarter on: 1,999 cores.
4. Fitted cell-store's hourly use on machines_in_service from c22_cell_hourly_2025-01-01_2026-12-13.csv and batch-train's hourly use, over the 17,081 hours on file with the re-sent day counted once: 33.1 plus 2.9404 per machine plus 0.20804 per batch core (residual s.d. 13.0 cores).
5. Read the fit at 5,220 machines with batch at its own guarantee, since CS-3 5.2 runs batch inside the guarantee, and solved CS-3 5.1 for it: (726,624 less 576,972 less 1,999 less 33.1 less 2.9404 x 5,220) / 1.20804 is 109,492, so the guarantee is 109,000.
6. Reserved cell-store at the 109,000 guarantee: 38,058 cores, reserved as 38,000, so the platform services reserve 40,000 with cell-ctl.
7. C-22 can guarantee 109,000 cores to batch training for 2027 Q1.

## 4. Deliverable Answers

### c22_capacity_2027q1.xlsx

1. Batch training guarantee, 2027 Q1: 109,000 cores
2. Reservations ahead of it:
   - Firm tenants: 577,000 cores
   - cell-store: 38,000 cores
   - cell-ctl: 2,000 cores
3. Batch training lost to preemptions, July to September 2026:
   - ranking-ml: 121,800 core-hours, 0.40% of the core-hours its runs held
   - pricing-ml: 80,500 core-hours, 0.37% of the core-hours its runs held
   - fraud-ml: 48,500 core-hours, 0.31% of the core-hours its runs held
   - reco-ml: 144,300 core-hours, 0.59% of the core-hours its runs held
   - demand-ml: 72,000 core-hours, 0.49% of the core-hours its runs held
   - nlp-ml: 134,900 core-hours, 0.77% of the core-hours its runs held
4. Machine-hours lost on machines that came back into service:
   - July 2026: hardware faults 750, planned maintenance 850
   - August 2026: hardware faults 730, planned maintenance 910
   - September 2026: hardware faults 660, planned maintenance 880
5. Owed under the chargeback policy for July to September 2026:
   - search-api: EUR 2,653,000
   - avail-cache: EUR 2,148,200
   - pricing: EUR 1,594,300
   - booking: EUR 1,204,900
   - payments: EUR 696,700
   - reviews: EUR 506,800
   - reco-serve: EUR 1,104,100
   - ads-listings: EUR 822,900
   - notify: EUR 409,200
   - partner-gw: EUR 658,500
   - settle-batch: EUR 488,500

### c22_capacity_review_2027q1.pptx

6. One slide: a stacked bar of the 726,624 reservable cores split into firm tenants 577,000, platform services 40,000 (cell-store 38,000, cell-ctl 2,000) and the batch training guarantee 109,000, titled with the guarantee, the axis in thousands of reservable cores.
