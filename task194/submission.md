# task194 submission

## Tags

**Domain:** Healthcare Delivery & Health Economics (provider quality and risk adjustment).
**Analytical objective:** Anomaly Detection & Diagnostics (separating the excess a unit is really carrying
from what measuring a few hundred episodes a quarter produces on its own).

## 1. Final Recommendation

**Place the cycle IP-10 improvement team with Alderbrook Orthopaedics, cost centre 41230.**

The placement avoids **21** hospital-acquired complications over the quarter from 1 April 2027, against
**13** at Alderbrook General Surgery, the closest unit, a gap of **8**. Alderbrook General Surgery will
record more complications next quarter than any other unit, but only **19.5** of them sit above its own
standing. Not Stonecreek Vascular Surgery, which stands worst of the twelve on its own record, because its
planned **506** separations carry only **14.8** complications above that standing and a placement there
avoids **10**. Not Alderbrook General Medicine, which is carrying **33** complications above expectation in
the December quarter, more than any other unit, while its own ten closed quarters put **4.9** above
expectation on the quarter's planned activity, so a placement there avoids **3**.

## 2. Critical Components

1. Units eligible for the cycle under charter clause 4.2: **12**
2. Alderbrook Orthopaedics' standardised ratio over the specification period: **1.16**
3. Expected complications its planned **2,200** separations carry for the quarter: **189**
4. Complications that planned activity carries above the unit's own standing: **31.1**

## 3. Step-by-Step Solution

1. Built each unit-quarter's observed and expected complications from episode_outcomes_extract.csv under
   specification 4.0 clauses 2.1 to 2.5 and 3.1, through drg_risk_bands.csv and hac_stratum_rates.csv; the
   result ties to unit_indicator_series.csv row for row.
2. Applied charter clause 4.2 through unit_register.csv and improvement_placements.csv: 12 eligible units.
3. Took each eligible unit's standardised ratio over the specification period, clause 3.3, which is the
   position clause 4.3 holds it to without the team: Alderbrook Orthopaedics stands at 1.16.
4. Converted the planned separations in activity_plan_2027q4.csv into each unit's expected complications for
   the quarter under clause 3.4: 189 at Alderbrook Orthopaedics on 2,200 planned separations.
5. Took what each unit's planned activity carries above its own standing: 31.1 complications at
   Alderbrook Orthopaedics, the largest of the 12.
6. Fitted the fall a placement produces to the eight closed placements in improvement_placements.csv, each
   measured against clause 4.3's position over its own quarters before the team arrived: the fall scales
   with the standing excess a unit carries, not with its expected complications or its level.
7. Applied that share to each unit's own excess: 21 complications avoided at Alderbrook Orthopaedics against
   13 at Alderbrook General Surgery.
8. Recommended the placement with Alderbrook Orthopaedics (41230) and wrote the per-unit table and the
   committee brief.

## 4. Deliverable Answers

### embed_placement_2027q4.xlsx

1. Recommendation: **Alderbrook Orthopaedics (41230)**; closest unit **Alderbrook General Surgery (41220)**; gap
   **8** complications.
2. Complications a placement would avoid, by unit, whole complications, in the file's order:
   - Alderbrook Orthopaedics (41230): 21
   - Alderbrook General Surgery (41220): 13
   - Marrowfield General Medicine (41420): 11
   - Stonecreek Vascular Surgery (41330): 10
   - Stonecreek General Medicine (41310): 8
   - Alderbrook Respiratory Medicine (41240): 5
   - Marrowfield Surgical Services (41520): 4
   - Alderbrook General Medicine (41210): 3
   - Carrowdean General Medicine (41510): 3
   - Stonecreek General Surgery (41320): 3
   - Marrowfield Orthopaedics (41410): 2
   - Stonecreek Renal Medicine (41430): 1

### embed_placement_brief.pdf

3. The case for Alderbrook Orthopaedics: standing 1.16, 189 expected complications on 2,200 planned
   separations, 31.1 above that standing, 21 avoided against 13 at the closest unit.
4. One bar for each eligible unit of the complications a placement there would avoid, in avoided order, the
   recommended unit marked, the axis in complications over the quarter and the finding as the title.

### Also requested

5. By hospital for the year ended 31 December 2026, in-scope episodes, complications and the adjusted rate
   per 1,000 episodes:
   - Alderbrook Hospital: 48,617 episodes, 5,488 complications, 114.7
   - Stonecreek Hospital: 26,869 episodes, 3,138 complications, 118.7
   - Marrowfield Hospital: 24,533 episodes, 2,676 complications, 120.0
   - Carrowdean District Hospital: 2,323 episodes, 229 complications, 109.4
6. By quarter, the separations the sub-acute and mental health units reported and the episodes among them
   that recorded a complication:
   - 2024-25 Q1: 913 separations, 45 with a complication
   - 2024-25 Q2: 800 separations, 45 with a complication
   - 2024-25 Q3: 844 separations, 47 with a complication
   - 2024-25 Q4: 930 separations, 55 with a complication
   - 2025-26 Q1: 930 separations, 41 with a complication
   - 2025-26 Q2: 825 separations, 46 with a complication
   - 2025-26 Q3: 839 separations, 41 with a complication
   - 2025-26 Q4: 915 separations, 54 with a complication
   - 2026-27 Q1: 931 separations, 37 with a complication
   - 2026-27 Q2: 817 separations, 59 with a complication
7. By complication group, the in-scope episodes that recorded one, 2025-26 and 2026-27 to 31 December 2026:
   - G1 Healthcare-associated infections: 2,826 and 1,368
   - G2 Pressure injuries: 1,926 and 884
   - G3 Falls resulting in fracture or intracranial injury: 1,684 and 849
   - G4 Medication and anaesthetic complications: 1,791 and 966
   - G5 Delirium: 2,064 and 1,102
   - G6 Respiratory complications: 2,272 and 1,159
   - G7 Venous thromboembolism: 1,175 and 536
   - G8 Surgical complications requiring unplanned return to theatre: 1,270 and 616
