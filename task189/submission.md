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
3. Cloonfad, Glasheen, Kilcrohane and Owenbeg exceed 0.05 ug/l under each of the **4** estimates that keep a bounded result bounded (a censored lognormal fit filling each bounded sample with its expected value below its own limit, Kaplan-Meier on the flipped sample, a fill from the sensitive method's quantified results below the limit, the same month's or the year's where the month has none, and the fitted lognormal's own mean), and every water body sits at least **11 per cent** clear of the standard under all four.
4. Ballynure, Derryvore and Tirneevin Stream are compliant, and each would be stated as non-compliant if half the reporting limit were written into its 35, 25 and 20 bounded results.
5. The return states **4** non-compliant water bodies of 13 assessed.

## 3. Step-by-Step Solution

1. Read lims_results_export_2025_2026.csv, kept the MCPA rows, joined client_point_code to the authority's monitoring point through monitoring_point_crosswalk.csv and to the water body through monitoring_programme_2025_26.xlsx.
2. Kept the FIELD rows (regulation 4.2 excludes the blanks, duplicates and spikes) and, per regulation 7.5, the latest approved version of each result.
3. Converted the Tirneevin rows from ng/l to ug/l on the units column, carrying each row's reporting_limit with it, and kept the samples collected between 1 April 2025 and 31 March 2026.
4. Took the 427 samples the programme requires for the 13 water bodies in the compliance network, each weighted equally as regulation 7.2 states.
5. Estimated each water body's annual average from those samples with each result below a limit kept as an unknown value under its own limit, never replaced by the limit or a fraction of it, and compared it with the 0.05 ug/l standard in Schedule 2.
6. Counted the water bodies above the standard: 4, against 7 if half of each reporting limit is substituted.
7. For ortho-phosphate, took the nutrient suite's approved results at the programme's points inside each point's programme dates, a point's compliance sample being the bottle filled on the visit that took its pesticide sample that month, so carrying that sample's collection date and time.
8. That visit identity settles the bookings that fall on no visit of the point they are booked to: a second booking of one bottle dated one to three days before the visit, the bottles booked first under a compliance point and later under the operational point that took them, and the Tirneevin nutrient bottles of operational points ARW-2122 and ARW-2241, whose codes ARWA-BN-22 and ARWA-CB-41 the crosswalk gives to ARW-0322 and ARW-1041; the counts by water body follow in block 4.

## 4. Deliverable Answers

### annual_compliance_return_2025_26.xlsx

1. Water bodies assessed as non-compliant for MCPA in 2025/26: **4** (Cloonfad, Glasheen, Kilcrohane, Owenbeg).
2. MCPA assessment, ortho-phosphate compliance samples with an approved result, and those results below the reporting limit, by water body:
   - Aghavannagh: compliant, 22, 10
   - Ballynure: compliant, 46, 22
   - Carrowbeg: compliant, 28, 11
   - Cloonfad: non-compliant, 35, 11
   - Derryvore: compliant, 34, 10
   - Drominagh: compliant, 35, 23
   - Glasheen: non-compliant, 35, 11
   - Kilcrohane: non-compliant, 23, 11
   - Knockanure: compliant, 34, 22
   - Lisheenaguile: compliant, 23, 11
   - Moneycashen: compliant, 23, 11
   - Owenbeg: non-compliant, 46, 23
   - Tirneevin Stream: compliant, 29, 11

### orthophosphate_results_2025_26.svg

3. One bar per water body, quantified ortho-phosphate results below and results below the reporting limit above, each bar labelled with its compliance samples: Aghavannagh 22 (10 below the limit), Ballynure 46 (22 below the limit), Carrowbeg 28 (11 below the limit), Cloonfad 35 (11 below the limit), Derryvore 34 (10 below the limit), Drominagh 35 (23 below the limit), Glasheen 35 (11 below the limit), Kilcrohane 23 (11 below the limit), Knockanure 34 (22 below the limit), Lisheenaguile 23 (11 below the limit), Moneycashen 23 (11 below the limit), Owenbeg 46 (23 below the limit), Tirneevin Stream 29 (11 below the limit).
