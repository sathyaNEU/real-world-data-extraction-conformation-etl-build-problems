# task194 submission

## Tags

**Domain:** Healthcare Delivery & Health Economics (provider quality and risk adjustment).
**Analytical objective:** Anomaly Detection & Diagnostics (separating the excess a unit is really
carrying from the excess the measurement system reports).

## 1. Final Recommendation

**Place the cycle IP-11 improvement team with Alderbrook Orthopaedics, cost centre 41230.**

The unit is carrying **40** avoidable hospital-acquired complications on the **2,305** separations it plans
for the quarter from 1 April 2027, against **25** at Marrowfield General Medicine, the closest unit, a gap of **15** complications,
**1.60** times and **2.41** standard errors of the gap. Not Alderbrook General Surgery, which the quarterly indicator puts first
with **59.2** complications above the published expectation on its planned activity: measured against the
complications its own patients would ordinarily have, it is carrying **-3**. Not Marrowfield General Medicine, which has the worst
avoidable rate at **23.0** per 1,000 separations against **17.4** here, because on the separations each
plans it is carrying **25** against **40**.

The stratum rates published with specification 4.0 were derived from activity in the year ended 30 June
2024 and clause 3.1 does not re-estimate them. The network's own rates now run from **0.887** to **1.313**
of them across the six risk bands, a factor of **1.48** that crosses 1.00 in both directions, while the
twelve candidates' surgical share of in-scope episodes runs from **0.075** to **0.851**. A ranking on the
published expectation therefore ranks case mix as much as practice. Marrowfield Orthopaedics, cost centre 41410, is the clearest
case: it treated the same number of patients in every closed quarter and changed nothing it does, and for
two of them its orthopaedic theatre was closed and its beds carried emergency general surgery. On the
published expectation its complications above expectation move from **1.1** to **9.4** a quarter, a
factor of **8.5**; on the complications its own patients would ordinarily have the figure holds between
**6.2** and **7.1** in every one of the ten quarters, a spread of **0.90** of a complication.

## 2. Critical Components

1. Units eligible for the cycle under charter clause 4.2: **12**
2. Alderbrook Orthopaedics's observed complications over the ten closed quarters: **1,795**
3. The complications patients of the same risk bands and age bands ordinarily have, over the same
   quarters and the same episodes: **1,466.3**
4. Its standardised ratio against that comparison: **1.22**, against **1.10** on the published rates
5. Avoidable complications on its **2,305** planned separations: **40**
6. Its rank on the published excess, which is the ranking the indicator report carries: **4** of **12**

## 3. Step-by-Step Solution

1. Built each unit-quarter's observed and published-expected complications from
   episode_outcomes_extract.csv under specification 4.0 clauses 2.1 to 2.5 and 3.1, through
   drg_risk_bands.csv and hac_stratum_rates.csv; the result ties to unit_indicator_series.csv row for
   row on all 215 unit-quarters.
2. Applied charter clause 4.2 through unit_register.csv and improvement_placements.csv: 12 eligible
   units.
3. Read charter clause 4.3: a unit's avoidable complications are the complications its own patients had,
   less the complications that patients of the same risk band and age band ordinarily have, counted
   patient by patient and summed over its episodes in the period, which specification 3.3 fixes as every
   closed quarter from 1 July 2024.
4. Tested whether the published stratum rates still are what such patients ordinarily have. They are not:
   Appendix A states they were derived from the year ended 30 June 2024, clause 3.1 does not re-estimate
   them, and the record's own frequency runs from 0.887 to 1.313 of them band by band. On the published
   expectation Marrowfield Orthopaedics's avoidable count moves by a factor of 8.5 across a quarter in which only its case mix
   changed, which is not a count of complications a unit carries as avoidable.
5. Measured the comparison from the record: complications per in-scope episode in each of the 24 strata,
   over the same ten closed quarters, from the same extract. Alderbrook Orthopaedics's episodes carry 1,466.3 on that
   basis against 1,627.0 on the published rates.
6. Carried each unit's own avoidable complications per separation onto the separations
   activity_plan_2027q4.csv plans for the quarter, which is clause 3.4's basis and clause 4.4's exposure:
   40 at Alderbrook Orthopaedics, the largest of the 12.
7. Measured each unit's excess against its own Poisson sampling error: 5.17 for 41230, 3.52 for 41420, 6.25 for
   the gap, so the lead is 2.41 standard errors and the top two are not inside one of each other.
8. Checked the ranking against every reading of clause 4.3 the text leaves open: the comparison
   frequency over the last eight, four or one closed quarter; the unit's own patients left out of the
   comparison; the unit's record over any of those windows; and the rate carried on in-scope episodes
   rather than on all separations. All **12** readings name the same unit, by between 1.14 and 2.86 times.
9. Recommended the placement with Alderbrook Orthopaedics (41230) and wrote the per-unit table and the committee brief.

## 4. Deliverable Answers

### embed_placement_2027q4.xlsx

1. Recommendation: **Alderbrook Orthopaedics (41230)**; closest unit **Marrowfield General Medicine (41420)**; gap **15** complications.
2. Avoidable complications by unit, whole complications, in the file's order:
   - Alderbrook Orthopaedics (41230): 40
   - Marrowfield General Medicine (41420): 25
   - Marrowfield Orthopaedics (41410): 8
   - Stonecreek Vascular Surgery (41330): 2
   - Stonecreek General Medicine (41310): 2
   - Stonecreek General Surgery (41320): 2
   - Carrowdean General Medicine (41510): 0
   - Marrowfield Surgical Services (41520): 0
   - Stonecreek Renal Medicine (41430): -1
   - Alderbrook Respiratory Medicine (41240): -2
   - Alderbrook General Surgery (41220): -3
   - Alderbrook General Medicine (41210): -5
3. Each unit's standardised ratio on the published rates and against the comparison frequency, to two
   decimals: Alderbrook Orthopaedics is 1.10 and 1.22.

### embed_placement_brief.pdf

4. The case for Alderbrook Orthopaedics: 1,795 observed complications against 1,466.3 the comparison gives its own patients, a
   standardised ratio of 1.22 against that comparison, 40 avoidable complications on 2,305 planned
   separations, against 25 at Marrowfield General Medicine, a gap of 15 complications, 1.60 times and 2.41 standard errors.
5. One bar for each eligible unit of its avoidable complications, in avoidable order, the recommended
   unit marked, the axis in avoidable complications on the quarter's planned separations and the finding
   as the title.

### Also requested

6. By hospital for the year ended 31 December 2026, in-scope episodes, complications and the adjusted
   rate per 1,000 episodes:
   - Alderbrook Hospital: 48,617 episodes, 4,909 complications, 102.6
   - Stonecreek Hospital: 26,848 episodes, 2,738 complications, 103.7
   - Marrowfield Hospital: 24,522 episodes, 2,294 complications, 103.9
   - Carrowdean District Hospital: 2,306 episodes, 199 complications, 111.7
7. By quarter, the separations the sub-acute and mental health units reported and the episodes among
   them that recorded a complication:
   - 2024-25 Q1: 901 separations, 45 with a complication
   - 2024-25 Q2: 793 separations, 45 with a complication
   - 2024-25 Q3: 832 separations, 46 with a complication
   - 2024-25 Q4: 918 separations, 54 with a complication
   - 2025-26 Q1: 908 separations, 41 with a complication
   - 2025-26 Q2: 808 separations, 45 with a complication
   - 2025-26 Q3: 819 separations, 40 with a complication
   - 2025-26 Q4: 900 separations, 53 with a complication
   - 2026-27 Q1: 917 separations, 37 with a complication
   - 2026-27 Q2: 809 separations, 58 with a complication
8. By complication group, the in-scope episodes that recorded one, 2025-26 and 2026-27 to 31 December
   2026:
   - G1 Healthcare-associated infections: 2,500 and 1,223
   - G2 Pressure injuries: 1,594 and 799
   - G3 Falls resulting in fracture or intracranial injury: 1,336 and 664
   - G4 Medication and anaesthetic complications: 1,688 and 775
   - G5 Delirium: 1,797 and 907
   - G6 Respiratory complications: 1,927 and 962
   - G7 Venous thromboembolism: 1,082 and 496
   - G8 Surgical complications requiring unplanned return to theatre: 1,250 and 639
