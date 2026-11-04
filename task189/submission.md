# task189 submission

## Tags

**Domain:** Physical & Environmental Sciences, environmental monitoring and exceedance (a river basin district's annual compliance return for a trace herbicide, assessed from a laboratory export in which most results carry only an upper bound).
**Analytical objective:** Anomaly Detection & Diagnostics (which apparent exceedances of the annual average standard are the water and which are the reporting limit of the method that measured it).

## 1. Final Recommendation

**The 2025/26 return has to state 4 water bodies as non-compliant for MCPA: Cloonfad, Glasheen, Kilcrohane and Owenbeg.**

Each water body's annual average was estimated from its own compliance samples, with every result the laboratory reported no value for kept as an observation bounded above by the limit that row carries rather than replaced by a value of any size. Three quarters of the year's MCPA results are bounded that way and the two methods in the programme report to 0.005 ug/l and 0.10 ug/l, so a substituted constant makes a water body's average a function of which laboratory holds its sample points: half the reporting limit states 7 water bodies, the limit itself 11, the non-detects dropped 8, and the non-detects treated as absent 3.

## 2. Critical Components

1. The reporting year holds **427** MCPA compliance samples at the programme's 37 points in 13 water bodies, of which **276** were reported below a reporting limit.
2. The two accredited methods report to **0.005 ug/l** (Tirneevin, LC-MS/MS, in ng/l) and **0.10 ug/l** (Kilgarron, GC-ECD), the second **twice** the 0.05 ug/l standard.
3. Cloonfad, Glasheen, Kilcrohane and Owenbeg exceed 0.05 ug/l under each of the **4** estimates that keep a bounded result bounded (a censored-sample fit filling each bounded sample at its own limit, Kaplan-Meier on the flipped sample, a fill from the sensitive method's quantified results of the same month, and the fitted lognormal's own mean), and every water body sits at least **11 per cent** clear of the standard under all four.
4. Ballynure, Derryvore and Tirneevin Stream are compliant, and each would be stated as non-compliant if half the reporting limit were written into its 35, 25 and 20 bounded results.
5. The return states **4** non-compliant water bodies of 13 assessed.

## 3. Step-by-Step Solution

1. Read lims_results_export_2025_2026.csv, kept the MCPA rows, joined client_point_code to the authority's monitoring point through monitoring_point_crosswalk.csv and to the water body through monitoring_programme_2025_26.xlsx.
2. Kept the FIELD rows (regulation 4.2 excludes the blanks, duplicates and spikes) and, per regulation 7.5, the latest approved version of each result.
3. Converted the Tirneevin rows from ng/l to ug/l on the units column, carrying each row's reporting_limit with it, and kept the samples collected between 1 April 2025 and 31 March 2026.
4. Took the 427 samples the programme requires for the 13 water bodies in the compliance network, each weighted equally as regulation 7.2 states.
5. Estimated each water body's annual average from those samples with each result below a limit held at its own limit, and compared it with the 0.05 ug/l standard in Schedule 2.
6. Counted the water bodies above the standard: 4, against 7 if half of each reporting limit is substituted.
7. For the abstraction points, put the Kilgarron nitrate results on the nitrate-ion basis, counted each round once where the water services and catchment sections both submitted it, and took each point's highest result and its rounds at or above 37.5 mg/l NO3.
8. For October to December 2025, counted the ortho-phosphate results the two quarterly reports list against those the export holds, and the sample identifiers in only one of the two.

## 4. Deliverable Answers

### annual_compliance_return_2025_26.xlsx

1. Water bodies assessed as non-compliant for MCPA in 2025/26: **4** (Cloonfad, Glasheen, Kilcrohane, Owenbeg).
2. Compliance samples in the year, results below the reporting limit, and assessment, by water body:
   - Aghavannagh: 23, 18, compliant
   - Ballynure: 47, 35, compliant
   - Carrowbeg: 30, 18, compliant
   - Cloonfad: 36, 11, non-compliant
   - Derryvore: 35, 25, compliant
   - Drominagh: 36, 31, compliant
   - Glasheen: 36, 19, non-compliant
   - Kilcrohane: 24, 5, non-compliant
   - Knockanure: 35, 28, compliant
   - Lisheenaguile: 24, 16, compliant
   - Moneycashen: 24, 19, compliant
   - Owenbeg: 47, 31, non-compliant
   - Tirneevin Stream: 30, 20, compliant

### mcpa_compliance_overview.png

3. One bar per water body, quantified results below and results below the reporting limit above, the four non-compliant water bodies marked: Owenbeg and Ballynure stand at 47 samples, Cloonfad, Drominagh and Glasheen at 36, Derryvore and Knockanure at 35, Carrowbeg and Tirneevin Stream at 30, Kilcrohane, Lisheenaguile and Moneycashen at 24, Aghavannagh at 23.

### Also requested

4. Raw-water abstraction points, highest nitrate result of the year as mg/l NO3 and rounds at or above 37.5 mg/l NO3:
   - Ballynure Borehole 1: 50.7, 14
   - Cloonfad Spring Chamber: 35.5, 0
   - Gortaleen Borehole: 65.9, 25
   - Moneycashen Intake: 28.5, 0
   - Rathvilly Borehole 2: 41.3, 3
   - Sheskin Shallow Well: 60.1, 19
5. Ortho-phosphate, October to December 2025: the quarterly reports list **250** results, the export holds **242**, and **18** sample identifiers sit in only one of the two.
