## Tags

**Domain:** Healthcare Delivery & Health Economics (utilization, access and demand forecasting: each member's 90th-percentile Hospital in the Home visit requirement for January to March 2027, built from planned admissions and the stays on file, against Bellbird Home Nursing's 850-visit overflow block).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Book Northgate 300 visits, Riverbend 250, Westmere 225 and Kingsdale 75 from Bellbird's January to March 2027 block, and Hillcrest none: the 850 visits run out at Kingsdale.**
Built from the operating plans' admissions by stream and the Alliance's stays, counted on the quarter's days, the 90th-percentile requirements are 2,400, 2,150, 1,800, 1,400 and 1,250 visits. Not the plan plus a Poisson margin, which treats each visit as an independent event and books 250 of the 850 visits (Northgate 100, Riverbend 50, Westmere 50, Kingsdale 25, Hillcrest 25); not the spread of past weeks, months or quarters, which treats those periods as independent and holds no bone and joint infection course at Northgate or Westmere.

## 2. Critical Components

1. Each member's 90th-percentile requirement for January to March 2027, to the nearest 50 visits: Northgate **2,400**, Riverbend **2,150**, Westmere **1,800**, Kingsdale **1,400**, Hillcrest **1,250**.
2. Above in-house capacity, Northgate needs **12** lots, Riverbend **10** and Westmere **9** (**775** visits), so Kingsdale takes the **3** lots left and Hillcrest none.

## 3. Step-by-Step Solution

1. Read the estimand in bellbird_agreement_schedule2_2027q1_block.pdf: a member's requirement is the nurse visits its admitted Hospital in the Home patients receive on 1 January to 31 March 2027, patients admitted before the quarter included for their days in it (clause 2.3); its expected value is the operating plan's January to March 2027 visits (2.5); lots of 25 cover the excess of the 90th percentile over in-house visits, booked in the clause 2.2 order until the 850 are used (2.6, 2.7).
2. Took the stays (admission to separation, both days) of completed episodes admitted 1 April 2024 to 30 June 2026 in hith_episodes_2024-04-01_to_2026-09-30.csv, codes used to 30 June 2025 mapped through hith_program_stream_crosswalk_2025-07.csv, pooled across members by stream; Northgate and Westmere, which open bone and joint infection on 1 October 2026 under the Alliance protocol (bji_at_home_pathway_northgate_westmere_2026.docx), take the Alliance's bone and joint stays.
3. Took each member's planned admissions by stream and month from October 2026 to March 2027 in hith_operating_plans_2026-27_rev_oct2026.xlsx, admissions arriving at random (Poisson) at each month's daily rate.
4. Counted the visits each admission's stay places on the quarter's days under hith_program_streams_and_visit_schedule_2025-07.pdf (wound care every second day, heart failure twice on each of the first two days), computed the exact distribution of each member's quarter total and read its 90th percentile, centred on the plans' expected visits (2,143, 1,905, 1,570, 1,209 and 1,064): 2,400, 2,150, 1,800, 1,400 and 1,250 to the nearest 50.
5. Subtracted the in-house visits in hith_inhouse_capacity_return_2027q1.xlsx (2,112, 1,911, 1,589, 1,246 and 1,086) and rounded each excess up to lots of 25: Northgate 12 lots, Riverbend 10, Westmere 9, Kingsdale more than the 3 left.
6. Booked in Schedule 2's order: Northgate 300 visits, Riverbend 250, Westmere 225, Kingsdale the last 75, Hillcrest none.

## 4. Deliverable Answers

### hith_overflow_block_2027q1.xlsx

1. Booking and 90th-percentile requirement for January to March 2027:
   - Northgate Health: 300 visits; requirement 2,400 visits
   - Riverbend Health: 250 visits; requirement 2,150 visits
   - Westmere Health: 225 visits; requirement 1,800 visits
   - Kingsdale Health: 75 visits; requirement 1,400 visits
   - Hillcrest Health: none; requirement 1,250 visits
2. What the Alliance owes Bellbird for July to September 2026:
   - Northgate Health: July $3,819; August $14,501; September $8,112
   - Riverbend Health: July $5,856; August $4,174; September $13,349
   - Westmere Health: July $4,474; August $6,436; September $6,143
   - Kingsdale Health: July $7,059; August $5,351; September $8,787
   - Hillcrest Health: July $2,652; August $6,641; September $7,163
3. Bellbird's referral response, July to September 2026:
   - Northgate Health: 56 referrals; 75.0% accepted within two hours; 94.1% of accepted referrals first visited within 24 hours
   - Riverbend Health: 43 referrals; 81.4%; 82.1%
   - Westmere Health: 40 referrals; 82.5%; 94.4%
   - Kingsdale Health: 45 referrals; 73.3%; 84.6%
   - Hillcrest Health: 37 referrals; 75.7%; 90.6%

### bellbird_weekly_visits_2026q3.png

4. The number of Bellbird's payable visits (completed or attempted) by pay week, weeks commencing Monday 29 June to Monday 28 September 2026, one panel per member and one for all members; quarter totals Northgate 161, Riverbend 140, Westmere 106, Kingsdale 130, Hillcrest 103.
