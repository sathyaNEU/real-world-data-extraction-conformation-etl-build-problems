# task194 submission

## Tags

**Domain:** Healthcare Delivery & Health Economics (provider quality and risk adjustment).
**Analytical objective:** Anomaly Detection & Diagnostics (separating the excess a unit is really carrying
from what measuring a few hundred episodes a quarter produces on its own).

## 1. Final Recommendation

**Place the cycle IP-10 improvement team with Alderbrook Orthopaedics, cost centre 41230.**

The placement avoids **17** hospital-acquired complications over the quarter from 1 April 2027, against
**11** at Alderbrook General Surgery, the closest unit, a gap of **6**. Not Alderbrook General Medicine,
which is carrying **34** complications above expectation in the December quarter, more of them than any
other unit, while its own ten closed quarters put **6** above expectation on the quarter's planned activity,
so a placement there avoids **2**. Not Stonecreek Vascular Surgery, which stands worst of the twelve on its
own record but whose planned **506** separations carry **16** complications above expectation, so a
placement there avoids **6**. Not Alderbrook General Surgery, which will record more complications than any
other unit next quarter, because **29** of them sit above its own expectation.

## 2. Critical Components

1. Units eligible for the cycle under charter clause 4.2: **12**
2. Alderbrook Orthopaedics' standardised ratio over the specification period: **1.23**
3. Expected complications its planned **2,305** separations carry for the quarter: **192**
4. Complications that planned activity carries above the unit's own standing: **44**

## 3. Step-by-Step Solution

1. Built each unit-quarter's observed and expected complications from episode_outcomes_extract.csv under
   specification 4.0 clauses 2.1 to 2.5 and 3.1, through drg_risk_bands.csv and hac_stratum_rates.csv; the
   result ties to unit_indicator_series.csv row for row.
2. Applied charter clause 4.2 through unit_register.csv and improvement_placements.csv: 12 eligible units.
3. Took each eligible unit's standardised ratio over the specification period, clause 3.3: Alderbrook
   Orthopaedics stands at 1.23 times its expected complications.
4. Converted the planned separations in activity_plan_2027q4.csv into each unit's expected complications for
   the quarter under clause 3.4: 192 at Alderbrook Orthopaedics on 2,305 planned separations.
5. Took what each unit's planned activity carries above its own standing: 44 complications at Alderbrook
   Orthopaedics, the largest of the twelve.
6. Priced a placement on the seven closed placements in improvement_placements.csv, each measured against
   what its unit stood at over its own closed quarters before the team arrived rather than against the
   quarter the placement was decided on.
7. Applied that share to each unit's own excess: 17 complications avoided at Alderbrook Orthopaedics against
   11 at Alderbrook General Surgery.
8. Recommended the placement with Alderbrook Orthopaedics (41230) and wrote the per-unit table and the
   committee brief.

## 4. Deliverable Answers

### embed_placement_2027q4.xlsx

1. Recommendation: **Alderbrook Orthopaedics (41230)**; closest unit **Alderbrook General Surgery
   (41220)**; gap **6** complications.
2. Complications a placement would avoid, by unit, whole complications, in the file's order:
   - Alderbrook Orthopaedics (41230): 17
   - Alderbrook General Surgery (41220): 11
   - Marrowfield General Medicine (41420): 9
   - Stonecreek General Medicine (41310): 7
   - Stonecreek Vascular Surgery (41330): 6
   - Alderbrook Respiratory Medicine (41240): 4
   - Carrowdean Surgical Services (41520): 3
   - Alderbrook General Medicine (41210): 2
   - Stonecreek General Surgery (41320): 2
   - Marrowfield Orthopaedics (41410): 2
   - Carrowdean General Medicine (41510): 2
   - Marrowfield Renal Medicine (41430): 1

### embed_placement_brief.pdf

3. The case for Alderbrook Orthopaedics: standing 1.23, 192 expected complications on 2,305 planned
   separations, 44 above that standing, 17 avoided against 11 at the closest unit.
4. One bar for each eligible unit of the complications a placement there would avoid, in avoided order, the
   recommended unit marked, the axis in complications over the quarter and the finding as the title.

### Also requested

5. By hospital for the year ended 31 December 2026, in-scope episodes, complications and the adjusted rate
   per 1,000 episodes:
   - Alderbrook Hospital: 36,993 episodes, 4,069 complications, 113.4
   - Stonecreek Hospital: 21,621 episodes, 2,432 complications, 115.8
   - Marrowfield Hospital: 15,037 episodes, 1,598 complications, 112.8
   - Carrowdean District Hospital: 2,304 episodes, 238 complications, 112.4
6. By quarter, the separations the sub-acute and mental health units reported and the episodes among them
   that recorded a complication:
   - 2024-25 Q1: 901 separations, 40 with a complication
   - 2024-25 Q2: 793 separations, 31 with a complication
   - 2024-25 Q3: 832 separations, 41 with a complication
   - 2024-25 Q4: 918 separations, 59 with a complication
   - 2025-26 Q1: 908 separations, 46 with a complication
   - 2025-26 Q2: 808 separations, 44 with a complication
   - 2025-26 Q3: 819 separations, 45 with a complication
   - 2025-26 Q4: 900 separations, 38 with a complication
   - 2026-27 Q1: 917 separations, 42 with a complication
   - 2026-27 Q2: 809 separations, 37 with a complication
7. By complication group, the in-scope episodes that recorded one, 2025-26 and 2026-27 to 31 December 2026:
   - G1 Healthcare-associated infections: 1,922 and 969
   - G2 Pressure injuries: 1,304 and 652
   - G3 Falls resulting in fracture or intracranial injury: 1,122 and 582
   - G4 Medication and anaesthetic complications: 1,252 and 643
   - G5 Delirium: 1,489 and 728
   - G6 Respiratory complications: 1,456 and 769
   - G7 Venous thromboembolism: 817 and 412
   - G8 Surgical complications requiring unplanned return to theatre: 955 and 465
