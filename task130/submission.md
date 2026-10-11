# task130: Tenter House, the replacement units for 1 April 2027

## Tags

**Domain:** Demographic & Social Science (housing: homelessness and temporary accommodation).
**Analytical objective:** Forecasting & Predictive Modeling (a closed group's run-off forecast from move-on lists worked against a planned supply).
**Reasoning phases:** Explore/Discover, Hypothesize, Analyze/Validate, Synthesize, Recommend/Communicate.

## 1. Final Recommendation

**Call off 52 replacement units for 1 April 2027: no one-bed, 10 two-bed, 18 three-bed and 24 four-bed.**

Of the 160 households in Tenter House on 30 September, 52 are still there on 31 March once each round's lets go by the bedrooms households need on the round day. Not the queue on the bedroom need on the case record, which has not caught up with children reaching ten or sixteen and keeps the longest-waiting households on lists they have left. Not the borough's recent leaving rate, which ignores the order lets are made in.

## 2. Critical Components

1. Households living in Tenter House at the end of 30 September 2026: **160**
2. Households expected still living there on 31 March 2027: **52**

## 3. Step-by-Step Solution

1. Took the households with a live Tenter House placement on 30 September 2026 from `ta_placements_2018-04_2026-09.csv`: 160, every one owed the main duty in `homelessness_cases_2026-09-30.csv`.
2. Worked out every open main-duty household's bedroom need under Part 3 of `housing_allocations_scheme_2024_parts_3_and_6.pdf` from the people in `household_members_2026-09-30.csv`, on each round day (3.4, 6.4), which reproduces all 49 lets accepted in the round of 21 September.
3. Listed every open main-duty case, households at home included, by duty acceptance date then case reference (6.1, 6.3), less the 49 households with October lets.
4. Ran the November to March rounds on the third Monday of the month before with the lets in the 14 September sheet of `moveon_plan_2026-27.xlsx`; no homes with five or more bedrooms are planned, so those households stay.
5. Counted the Tenter House households no round reaches, each under the unit it needs on 1 April 2027 (closure procedure, point 5): 52.
6. Priced the call-off at the Lot 3 2027/28 weekly rates in `dps_lot2_lot3_price_schedule.xlsx`: GBP 24,512 a week.
7. Recommendation: call off 52 units for 1 April 2027 (0 one-bed, 10 two-bed, 18 three-bed, 24 four-bed).

## 4. Deliverable Answers

### tenter_house_replacement_units.xlsx

1. Units to call off for 1 April 2027, whole units:
   - One-bed: 0
   - Two-bed: 10
   - Three-bed: 18
   - Four-bed (four or more): 24
   - Total: 52
2. Weekly cost of the call-off at the Lot 3 rates from 1 April 2027: GBP 24,512
3. Households expected still living in Tenter House at each month end, by the size of replacement unit each will move into, whole households:
   - One-bed: 31 Oct 2026 20, 30 Nov 2026 10, 31 Dec 2026 4, 31 Jan 2027 0, 28 Feb 2027 0, 31 Mar 2027 0
   - Two-bed: 31 Oct 2026 49, 30 Nov 2026 41, 31 Dec 2026 35, 31 Jan 2027 26, 28 Feb 2027 18, 31 Mar 2027 10
   - Three-bed: 31 Oct 2026 43, 30 Nov 2026 38, 31 Dec 2026 35, 31 Jan 2027 31, 28 Feb 2027 26, 31 Mar 2027 18
   - Four-bed: 31 Oct 2026 31, 30 Nov 2026 30, 31 Dec 2026 30, 31 Jan 2027 29, 28 Feb 2027 26, 31 Mar 2027 24

### tenter_house_runoff.png

1. Stacked bars of households in Tenter House by replacement unit size at 30 September 2026 and each month end to 31 March 2027 (totals 160, 143, 119, 104, 86, 70, 52), the call-off of 52 units (0, 10, 18 and 24 by size) annotated at March.
2. Title: Call off 52 replacement units for 1 April 2027: Tenter House runs down from 160 households to 52
