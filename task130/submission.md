# task130: Tenter House, the replacement units for 1 April 2027

## Tags

**Domain:** Demographic & Social Science (housing: homelessness and temporary accommodation).
**Analytical objective:** Forecasting & Predictive Modeling (a closed group's run-off forecast from a move-on list worked against a planned supply).
**Reasoning phases:** Explore/Discover, Hypothesize, Analyze/Validate, Synthesize, Recommend/Communicate.

## 1. Final Recommendation

**Call off 46 replacement units for 1 April 2027: no one-bed, 7 two-bed, 20 three-bed and 19 four-bed.**

Of the 170 households in Tenter House on 30 September, 46 are still there on 31 March, because the move-on plan's lets reach most of the block's households, who sit near the front of their size's list. Not a unit for every household now in the block, which ignores six months of lets. Not the borough's recent monthly leaving rate, which treats the block's households as average members of their lists.

## 2. Critical Components

1. Households living in Tenter House on 30 September 2026: **170** (28 one-bed, 66 two-bed, 50 three-bed, 26 four-bed need)
2. Households expected still living there on 31 March 2027: **46**

## 3. Step-by-Step Solution

1. Took the households with a live Tenter House placement on 30 September 2026 from `ta_placements_2018-04_2026-09.csv`: 170, every one owed the main duty in `homelessness_cases_2026-09-30.csv`.
2. Set each case's current bedroom need from its latest review in `bedroom_need_reviews.csv`, else the need at decision, as the closure procedure (point 5) requires: 28, 66, 50 and 26 households needing one to four bedrooms.
3. Replayed `moveon_lets_2018-04_2026-09.csv`: every one of the 5,262 lets since April 2018 went to the front of its size's list of open main-duty cases, wherever the household lived, ordered by duty acceptance date and then case reference.
4. Built each size's list on 30 September from every open main-duty case, households at home included, with the October lets already accepted at its front.
5. Worked the revised move-on plan in `moveon_plan_2026-27.xlsx` (sheet of 14 September, October counting accepted lets) down each list month by month: 89, 117, 56 and 19 lets reach the first that many households of the one- to four-bed lists.
6. Counted the Tenter House households beyond each month's reach: 46 remain on 31 March 2027.
7. Priced the call-off at the Lot 3 2027/28 weekly rates in `dps_lot2_lot3_price_schedule.xlsx`: GBP 21,615 a week.
8. Recommendation: call off 46 units for 1 April 2027 (0 one-bed, 7 two-bed, 20 three-bed, 19 four-bed).

## 4. Deliverable Answers

### tenter_house_calloff_2027.xlsx

1. Units to call off for 1 April 2027, whole units:
   - One-bed: 0
   - Two-bed: 7
   - Three-bed: 20
   - Four-bed (four or more): 19
   - Total: 46
2. Weekly cost of the call-off at the Lot 3 rates from 1 April 2027: GBP 21,615
3. Households expected still living in Tenter House at each month end, by bedroom need, whole households:
   - One-bed: 31 Oct 2026 20, 30 Nov 2026 13, 31 Dec 2026 8, 31 Jan 2027 0, 28 Feb 2027 0, 31 Mar 2027 0
   - Two-bed: 31 Oct 2026 57, 30 Nov 2026 46, 31 Dec 2026 42, 31 Jan 2027 32, 28 Feb 2027 21, 31 Mar 2027 7
   - Three-bed: 31 Oct 2026 46, 30 Nov 2026 42, 31 Dec 2026 38, 31 Jan 2027 34, 28 Feb 2027 29, 31 Mar 2027 20
   - Four-bed: 31 Oct 2026 26, 30 Nov 2026 25, 31 Dec 2026 24, 31 Jan 2027 23, 28 Feb 2027 21, 31 Mar 2027 19

### tenter_house_runoff.png

1. Stacked bars of households in Tenter House by bedroom need at 30 September 2026 and each month end to 31 March 2027 (totals 170, 149, 126, 112, 89, 71, 46), the call-off of 46 units (0, 7, 20 and 19 by size) annotated at March.
2. Title: Call off 46 replacement units for 1 April 2027: Tenter House runs down from 170 households to 46
