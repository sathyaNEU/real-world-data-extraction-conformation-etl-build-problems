# task194 submission

## Tags

**Domain:** Healthcare Delivery & Health Economics (provider quality and risk adjustment).
**Analytical objective:** Anomaly Detection & Diagnostics (separating the excess a unit is really carrying
from what measuring a few hundred episodes a quarter produces on its own).

## 1. Final Recommendation

**Place the cycle IP-10 improvement team with Alderbrook Orthopaedics, cost centre 41230.**

The placement avoids **18** hospital-acquired complications over the quarter from 1 April 2027, against
**12** at Alderbrook General Surgery, the closest unit, a gap of **6**. Not Alderbrook General Medicine, which is
carrying **36** complications above expectation in the December quarter, more than any other unit,
while its own ten closed quarters put **5.6** above expectation on the quarter's planned activity, so a
placement there avoids **2**. Not Stonecreek Vascular Surgery, which stands worst of the twelve on its
own record but whose planned **508** separations carry **14.8** complications above expectation, so
a placement there avoids **6**. Not Alderbrook General Surgery, which will record more complications
than any other unit next quarter, because only **30.6** of them sit above its own expectation.

## 2. Critical Components

1. Units eligible for the cycle under charter clause 4.2: **12**
2. Alderbrook Orthopaedics' standardised ratio over the specification period: **1.23**
3. Expected complications its planned **2,359** separations carry for the quarter: **204**
4. Complications that planned activity carries above the unit's own standing: **46.4**

## 3. Step-by-Step Solution

1. Built each unit-quarter's observed and expected complications from episode_outcomes_extract.csv under
   specification 4.0 clauses 2.1 to 2.5 and 3.1, through drg_risk_bands.csv and hac_stratum_rates.csv; the
   result ties to unit_indicator_series.csv row for row.
2. Applied charter clause 4.2 through unit_register.csv and improvement_placements.csv: 12 eligible units.
3. Took each eligible unit's standardised ratio over the specification period, clause 3.3: Alderbrook Orthopaedics
   stands at 1.23 times its expected complications.
4. Converted the planned separations in activity_plan_2027q4.csv into each unit's expected complications for
   the quarter under clause 3.4: 204 at Alderbrook Orthopaedics on 2,359 planned separations.
5. Took what each unit's planned activity carries above its own standing: 46.4 complications at
   Alderbrook Orthopaedics, the largest of the 12.
6. Priced a placement on the 7 closed placements in improvement_placements.csv, each measured against
   what its unit stood at over its own closed quarters before the team arrived rather than against the
   quarter the placement was decided on.
7. Applied that share to each unit's own excess: 18 complications avoided at Alderbrook Orthopaedics against
   12 at Alderbrook General Surgery.
8. Recommended the placement with Alderbrook Orthopaedics (41230) and wrote the per-unit table and the committee
   brief.

## 4. Deliverable Answers

### embed_placement_2027q4.xlsx

1. Recommendation: **Alderbrook Orthopaedics (41230)**; closest unit **Alderbrook General Surgery (41220)**; gap
   **6** complications.
2. Complications a placement would avoid, by unit, whole complications, in the file's order:
   - Alderbrook Orthopaedics (41230): 18
   - Alderbrook General Surgery (41220): 12
   - Marrowfield General Medicine (41420): 8
   - Stonecreek General Medicine (41310): 6
   - Stonecreek Vascular Surgery (41330): 6
   - Alderbrook Respiratory Medicine (41240): 4
   - Marrowfield Surgical Services (41520): 3
   - Alderbrook General Medicine (41210): 2
   - Carrowdean General Medicine (41510): 2
   - Marrowfield Orthopaedics (41410): 1
   - Stonecreek General Surgery (41320): 1
   - Stonecreek Renal Medicine (41430): 1

### embed_placement_brief.pdf

3. The case for Alderbrook Orthopaedics: standing 1.23, 204 expected complications on 2,359 planned
   separations, 46.4 above that standing, 18 avoided against 12 at the closest unit.
4. One bar for each eligible unit of the complications a placement there would avoid, in avoided order, the
   recommended unit marked, the axis in complications over the quarter and the finding as the title.

### Also requested

5. By hospital for the year ended 31 December 2026, in-scope episodes, complications and the adjusted rate
   per 1,000 episodes:
   - Alderbrook Hospital: 38,249 episodes, 4,017 complications, 109.0
   - Stonecreek Hospital: 23,179 episodes, 2,525 complications, 112.2
   - Marrowfield Hospital: 19,733 episodes, 2,016 complications, 110.3
   - Carrowdean District Hospital: 2,340 episodes, 234 complications, 111.6
6. By quarter, the separations the sub-acute and mental health units reported and the episodes among them
   that recorded a complication:
   - 2024-25 Q1: 901 separations, 50 with a complication
   - 2024-25 Q2: 793 separations, 42 with a complication
   - 2024-25 Q3: 832 separations, 44 with a complication
   - 2024-25 Q4: 918 separations, 46 with a complication
   - 2025-26 Q1: 908 separations, 37 with a complication
   - 2025-26 Q2: 808 separations, 36 with a complication
   - 2025-26 Q3: 819 separations, 42 with a complication
   - 2025-26 Q4: 900 separations, 50 with a complication
   - 2026-27 Q1: 917 separations, 47 with a complication
   - 2026-27 Q2: 809 separations, 47 with a complication
7. By complication group, the in-scope episodes that recorded one, 2025-26 and 2026-27 to 31 December 2026:
   - G1 Healthcare-associated infections: 2,070 and 997
   - G2 Pressure injuries: 1,410 and 686
   - G3 Falls resulting in fracture or intracranial injury: 1,263 and 658
   - G4 Medication and anaesthetic complications: 1,447 and 725
   - G5 Delirium: 1,633 and 825
   - G6 Respiratory complications: 1,683 and 808
   - G7 Venous thromboembolism: 866 and 430
   - G8 Surgical complications requiring unplanned return to theatre: 1,058 and 478
