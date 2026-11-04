## Tags

**Domain:** General statistics and data science (data integration, record linkage and entity resolution), for a utility's fuel stock (house domain: business and operations analytics).
**Analytical objective:** Data extraction and conformation (ETL).

## 1. Final Recommendation

**Do not nominate Silesia's winter option cargo: the coal yard held 150,000 t at the 16 December survey, 62 days of the first-quarter burn plan against the 60-day floor.** The reserve clears the floor by 4,000 t. Not a base drawn through each pile's toe, the stock surveyor's usual base: under the five long-standing pile areas the pad has settled into a bowl up to about two metres below the toe, as the surveys that recorded each area bare show, so a toe base leaves the coal in the bowl out of the reserve.

## 2. Critical Components

1. Each pile area's pad is the surface the 2026 surveys recorded with the area bare, not a plane through the toe: P1 18 March, P2 15 April, P3 17 June, P4 14 October, P5 13 May, P6 13 May.
2. The reserve is **150,000 t**.
3. The planned burn is **2,430 t a day** (218,740 t over 90 days).
4. Days of cover: **62**, 4,000 t above the floor of 146,000 t.

## 3. Step-by-Step Solution

1. Took every survey onto the 16 December 2026 survey's points with survey_control_report_2026-07.pdf (the plant grid's rotation and offset, N2000 = N60 + 0.384 m) and gave each point to its pile area in coalyard_pile_areas.csv, each area to half the gap to the next.
2. For each area took as its pad the latest survey before December in which the area was bare (P1 18 March, P2 15 April, P3 17 June, P4 14 October, P5 13 May, P6 13 May), up to about two metres below the pile's toe under the long-standing areas.
3. Multiplied each area's volume above that pad by the latest fuel_lab_density_tests.csv density before the survey (PR-07 3.2) and summed: 150,000 t.
4. Divided by the plan's 218,740 t over 90 days in coal_burn_plan_2027Q1.xlsx (PR-07 3.3): 62 days, 4,000 t above the 60-day floor, so no nomination (PR-07 5).
5. Receipts (OH-12 1.1): each call's CV-01 intervals while gu1_unloader_events.csv shows GU-1 running, between the two December flights, plus each historian catch-up whose link fell while that call discharged, by coal_contracts.csv: KH-COL 144,000 t; KH-POL 286,000 t; KH-USA 176,000 t.
6. Deliveries (OH-12 1.2, 2.1): CV-21 between the shift log's readings at 00:00 on each quarter's first day (the June integrator restart bridged), less the CV-21 blocks run while CV-01 carried coal with GU-1 stopped (the crossover): Q1 218,000 t; Q2 112,000 t; Q3 43,000 t; Q4 217,000 t.
7. Let the winter option lapse: 150,000 t and 62 days against the 60-day floor.

## 4. Deliverable Answers

### coal_reserve_2026.xlsx

1. Each pile area at the 16 December 2026 survey, volume to the nearest 1,000 m3 and tonnes to the nearest 1,000:
   - P1 (KH-COL): 32,000 m3, 29,000 t
   - P2 (KH-COL): 32,000 m3, 28,000 t
   - P3 (KH-POL): 29,000 m3, 26,000 t
   - P4 (KH-USA): 28,000 m3, 26,000 t
   - P5 (KH-POL): 24,000 m3, 21,000 t
   - P6 (KH-USA): 21,000 m3, 20,000 t
2. Reserve: 150,000 t
3. Days of cover: 62
4. Call: do not nominate the winter option cargo; it lapses on 8 January 2027
5. Coal received into the yard between the December 2025 and December 2026 surveys:
   - KH-COL: 144,000 t
   - KH-POL: 286,000 t
   - KH-USA: 176,000 t
6. Coal sent to the boiler house in 2026:
   - Q1: 218,000 t
   - Q2: 112,000 t
   - Q3: 43,000 t
   - Q4: 217,000 t

### coalyard_stock_2026.svg

1. Line chart of the coal in the yard at every survey from 17 December 2025 to 16 December 2026, each survey's coal taken above the same pads and at the laboratory's latest density before that survey (PR-07 3.2's rule applied to every survey), with the 60-day floor (146,000 t) drawn across it and the December 2026 point at 150,000 t, 62 days.
