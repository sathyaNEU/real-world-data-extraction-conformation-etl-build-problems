**Domain:** Healthcare Delivery & Health Economics (provider quality and risk adjustment).
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**Place the cycle IP-11 improvement team with Alderbrook General Medicine, cost centre 41210.**
It carries 44.6 avoidable complications on the 4,261 separations planned for the quarter from 1 April
2027, against 27.8 at the closest unit, a margin of 1.604x. Not Alderbrook General Surgery (41220), which
leads on the complications the extract records today at 26.1 and falls to 27.8 once every cost centre's
quarters are carried to what they will reach. Not Stonecreek General Surgery (41320), which leads on the
four most recent closed quarters at 27.59 because those are the quarters the pull date cuts shortest.

## 2. Critical Components

1. Four of the ten closed quarters are still being added to, and the coding close-out register names them: **2025-26 Q2, 2025-26 Q3, 2025-26 Q4 and 2026-27 Q1**
2. A quarter of cost centre 41210's coding carries **1.763** of its eventual count at its own close, against **1.0368** at cost centre 41220
3. Developing 41210's short quarters on its own record takes its ten quarters from 3097 to **3408.5** complications, an uplift of **311.5**
4. Against the published stratum table's **3023.6** expected complications, that is **44.6** avoidable complications on the quarter's planned separations
5. On the complications the extract records today 41210 reads **5** of 12, which is why the record as it stands does not point at it

## 3. Step-by-Step Solution

1. Applied specification 4.0 clauses 2.1 to 2.4 to `episode_outcomes_extract.csv`, joined `drg_risk_bands.csv` and `hac_stratum_rates.csv`, and reconciled every unit-quarter to `unit_indicator_series.csv`.
2. Applied charter clause 4.2 through `unit_register.csv` and `improvement_placements.csv`: 12 eligible units.
3. Read `coding_close_out_register.csv`, which publishes each quarter at its coding close and restates it at every close after: a quarter whose last two publications agree has settled, and 4 of the 10 have not.
4. Measured each cost centre's growth from its own finished quarters, the count at each publication against the count it settled at: 1.763 at cost centre 41210 against 1.0368 at cost centre 41220.
5. Carried each unit's short quarters by its own factor: 41210's ten quarters reach 3408.5 complications, an uplift of 311.5.
6. Took the expected complications of specification 3.1 and Appendix A over the same episodes, 3023.6 for 41210, and carried the difference onto the planned separations of `activity_plan_2027q4.csv` under specification 3.4.
7. Ranked the 12: 44.6 at cost centre 41210 against 27.8 at cost centre 41220, and confirmed all 5 readings of the growth name the same unit, by between 1.528 and 1.608 times.
8. Place the team with Alderbrook General Medicine, cost centre 41210.

## 4. Deliverable Answers

### embed_placement_2027q4.xlsx

1. Avoidable complications on the quarter's planned separations, all 12 eligible units, to one decimal:
   - Cost centre 41210, Alderbrook General Medicine: 44.6 on 4,261 planned separations
   - Cost centre 41220, Alderbrook General Surgery: 27.8 on 4,754 planned separations
   - Cost centre 41230, Alderbrook Orthopaedics: 18.5 on 3,098 planned separations
   - Cost centre 41320, Stonecreek General Surgery: 14.9 on 2,100 planned separations
   - Cost centre 41410, Marrowfield Orthopaedics: 12.9 on 1,098 planned separations
   - Cost centre 41240, Alderbrook Respiratory Medicine: 11.6 on 1,704 planned separations
   - Cost centre 41520, Marrowfield Surgical Services: 6.9 on 1,099 planned separations
   - Cost centre 41330, Stonecreek Vascular Surgery: 6.4 on 834 planned separations
   - Cost centre 41310, Stonecreek General Medicine: 4.9 on 2,009 planned separations
   - Cost centre 41420, Marrowfield General Medicine: 4.3 on 1,599 planned separations
   - Cost centre 41430, Stonecreek Renal Medicine: 3.2 on 960 planned separations
   - Cost centre 41510, Carrowdean General Medicine: 1.9 on 711 planned separations
2. The recommendation: Alderbrook General Medicine, cost centre 41210, at 44.6; closest unit Alderbrook General Surgery, cost centre 41220, at 27.8; gap 16.8.
3. Separations the complication indicator does not measure in the year to 31 December 2026, and how many of those recorded a complication, whole separations:
   - Alderbrook Hospital: 7198 not measured, 383 with a complication
   - Stonecreek Hospital: 6108 not measured, 369 with a complication
   - Marrowfield Hospital: 6715 not measured, 421 with a complication
   - Carrowdean District Hospital: 1914 not measured, 145 with a complication
4. Separations the sub-acute and mental health units reported, and the episodes with a complication, by quarter, whole separations:
   - 2024-25 Q1: 1443 separations, 107 with a complication
   - 2024-25 Q2: 1269 separations, 103 with a complication
   - 2024-25 Q3: 1332 separations, 115 with a complication
   - 2024-25 Q4: 1470 separations, 114 with a complication
   - 2025-26 Q1: 1451 separations, 97 with a complication
   - 2025-26 Q2: 1293 separations, 98 with a complication
   - 2025-26 Q3: 1310 separations, 93 with a complication
   - 2025-26 Q4: 1441 separations, 116 with a complication
   - 2026-27 Q1: 1468 separations, 107 with a complication
   - 2026-27 Q2: 1295 separations, 116 with a complication
5. In-scope episodes recording a complication by complication group, whole episodes:
   - G1 Healthcare-associated infections: 3563 in 2025-26, 1618 in 2026-27 to date
   - G2 Pressure injuries: 4281 in 2025-26, 2104 in 2026-27 to date
   - G3 Falls resulting in fracture or intracranial injury: 1827 in 2025-26, 837 in 2026-27 to date
   - G4 Medication and anaesthetic complications: 1598 in 2025-26, 704 in 2026-27 to date
   - G5 Delirium: 4236 in 2025-26, 1892 in 2026-27 to date
   - G6 Respiratory complications: 2613 in 2025-26, 1264 in 2026-27 to date
   - G7 Venous thromboembolism: 861 in 2025-26, 425 in 2026-27 to date
   - G8 Surgical complications requiring unplanned return to theatre: 1661 in 2025-26, 757 in 2026-27 to date

### embed_placement_brief.pdf

1. The recommendation on page 1: place the team with Alderbrook General Medicine, cost centre 41210, at 44.6 avoidable complications, 16.8 more than the closest unit.
2. One horizontal bar per eligible unit of the avoidable complications it carries, the recommended unit marked, on page 1.
