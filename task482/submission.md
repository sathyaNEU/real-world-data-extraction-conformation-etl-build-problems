## Tags

**Domain:** Healthcare Delivery & Health Economics, payment, claims and health plan analytics (a clinically integrated network's 2027 two-sided risk elections for its thirteen primary care practices, conformed from three commercial payers' claim, coverage and attribution feeds in three layouts, the network's clinician roster and master patient index, its performance standard and the payers' E&M fee schedules).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Enter Ostrelwood, Callowglen, Thornelfield, Birrelhaven, Raddelview, Jesselford, Nerrincreek and Torrinridge in the 2027 two-sided track and keep Haddelcrest, Wexelmoor, Mallowcrest, Prestelglen and Garrowdale one-sided.**
Mallowcrest and Garrowdale come in over their thresholds once the seven members still in hospital on 31 August 2026, each already past the USD 250,000 cap, are carried at it. Not Ostrelwood, Thornelfield and Jesselford alone, the interim measure as it stands: the October runs attribute only the members whose qualifying visit has been paid. Not Mallowcrest and Garrowdale as well, the interim measure carried by each practice's own 2025 run-out alone: a hospital bills a stay when it ends, so neither the completion factors nor the run-out carries a stay still running at the cut.

## 2. Critical Components

1. Members in a hospital stay still running on 31 August 2026 and already past the USD 250,000 cap: **seven**, three at Mallowcrest Pediatrics and four at Garrowdale Family Practice.
2. 2026 thresholds, 98 per cent of the benchmark: Mallowcrest **USD 179.67** and Garrowdale **USD 454.16**.

## 3. Step-by-Step Solution

1. Conformed the three payers' claims at their current version (Merrinlake's voided originals out, Kesselcrest's superseded claims (status A) out and its cents in dollars, Pemberglen's latest version), member months from the coverage files, and every run's TIN to its practice through lpn_primary_care_roster_2026-10.xlsx.
2. Took each practice's 2025 network measure on the payers' final 2025 runs (standard, section 3: claims first paid by 31 March 2026, each member's year capped at USD 250,000) and its threshold at 98 per cent of its benchmark, the measure to the cent times 1.052 to the cent (section 3.4).
3. Computed each practice's interim measure on the October runs (section 4.1, the factors in payer_completion_factors_2026-09.csv): taken as the 2026 figure it enters Ostrelwood, Thornelfield and Jesselford alone.
4. Re-ran the standard's attribution (section 2) on the 2025 professional claims at the October run's cut, qualifying services incurred by 31 August 2025 and paid by 30 September 2025, and carried each practice's interim measure by its 2025 measure over the January to August 2025 measure of the members so attributed (no long stay was running at the 2025 cut): ten practices come in under.
5. Found the members in a stay still running at the cut (their attending physicians' daily inpatient visits run to the cut with no facility claim in the October feeds): at the lowest per-day amount any closed stay of a month or more of the same kind was allowed, seven had passed the USD 250,000 cap; carried at the cap with each one's months of coverage in the year, Mallowcrest and Garrowdale come in over their thresholds.
6. For the level 5 share, read each visit's paid level from its claim's allowed amount, every line of the claim counted, against the payer's 2026 rate for its setting in payer_em_fee_schedules_2026.xlsx: a Kesselcrest 99215 claim whose line with no procedure code takes it down to Kesselcrest's 99214 rate is level 4, and a Merrinlake E&M billed with modifier 25 beside a minor procedure by the same clinician that day is at the level whose rate is twice its allowed amount (a halved 99215 equals Merrinlake's 99213 rate), a modifier 25 visit beside a preventive visit at its own rate.
7. Entered the eight practices under their thresholds in the two-sided track for 2027.

## 4. Deliverable Answers

### two_sided_track_elections_2027.xlsx

1. Elections, one row per practice:
   - Ostrelwood Internal Medicine: two-sided
   - Callowglen Family Practice: two-sided
   - Thornelfield Family Medicine: two-sided
   - Haddelcrest Internal Medicine: one-sided
   - Birrelhaven Children's Clinic: two-sided
   - Raddelview Family Physicians: two-sided
   - Jesselford Family Medicine: two-sided
   - Nerrincreek Family Practice: two-sided
   - Wexelmoor Internal Medicine: one-sided
   - Torrinridge Family Medicine: two-sided
   - Mallowcrest Pediatrics: one-sided
   - Prestelglen Internal Medicine: one-sided
   - Garrowdale Family Practice: one-sided
2. Share of established-patient visits January to August 2026 the payers paid at level 5, per cent:
   - Ostrelwood Internal Medicine: 18.6
   - Callowglen Family Practice: 15.5
   - Thornelfield Family Medicine: 17.3
   - Haddelcrest Internal Medicine: 18.4
   - Birrelhaven Children's Clinic: 8.9
   - Raddelview Family Physicians: 17.1
   - Jesselford Family Medicine: 17.6
   - Nerrincreek Family Practice: 15.7
   - Wexelmoor Internal Medicine: 19.8
   - Torrinridge Family Medicine: 16.7
   - Mallowcrest Pediatrics: 8.7
   - Prestelglen Internal Medicine: 19.9
   - Garrowdale Family Practice: 16.5

### practice_cost_vs_benchmark_2026.png

1. Horizontal bar chart of each practice's projected 2026 network measure against its threshold: the eight entering practices' bars fall below the threshold line and the five one-sided practices' bars above it.
