# Determinism check, task452

Two isolated judge threads (Sonnet, medium effort), each on a fresh unzip of target.zip with the prompt, the submission's graded blocks and the judge's system prompt verbatim; neither saw the design note, the generator or the other's report.

## Pass 1 (2026-10-13), on the first cut


**Verdict:** DETERMINISTIC (main call), with two flagged weaknesses on supplementary answers (Q2 rounding, Q6 acreage source). No SOLUTION_WRONG: every claimed figure reproduced.

**Disposition:** FIX_NOW. Pin the cover crop apportionment in the prompt (or relabel the contracts file's `watershed` column) and have the rubric grade the Q2 loads as ranges; the main call, the stump and the data stay as they are. Only supplementary Q6 (and the Q2 grading tolerance) need a rerun check; no main-call rerun.

**Why:** The three largest exceedances (Kestle River, Hessick River, Varrow Brook) hold under every rating-curve variant I ran (seasonal or not, quadratic, normal or Duan retransformation, BLC-only samples, added time trend, shorter fits). The gap to the fourth tributary (Ambrey River, about +350 kg) is more than 3 times the margin to Varrow (about +1,120 kg). The method is not filed, but the data separates the candidates: leave-one-out error in log concentration is about 0.26 to 0.35 for the rating curve against 0.45 to 1.0 for sample-to-sample interpolation at all ten stations, so the interpolation set (Ambrey, Orrinwood, Varrow) is the weaker estimator, not an equal alternative.

### Recomputation ledger

Method used: TP (fraction Total), routine, Accepted, BLC plus ACWL (ACWL ids mapped through the register), ug/L to mg/L; daily mean Q = approved 15-min values averaged over Eastern calendar days (WY2026) and the approved daily file (WY2024-25); Dunmarsh Q scaled 61.4/52.8; log C on log Q + sin/cos(doy) on every sample, Duan smearing, sum of C x Q x 2.44660 kg/d per cfs-mg/L.

| Figure | Claimed | Recomputed | Reproduced |
|---|---|---|---|
| Samples per station | 79 to 81 | 79,80,81,80,79,80,79,80,79,80 | yes |
| Kestle load | 16,820 | 16,817.5 | yes |
| Hessick load | 6,910 | 6,906.3 | yes |
| Varrow load | 4,360 | 4,364.0 | yes |
| Ambrey load | 3,730 | 3,731.6 | yes |
| Orrinwood load | 2,600 | 2,603.8 | yes |
| Pellow load | 740 | 735.3 | yes (on a rounding edge) |
| Fallowmere load | 1,070 | 1,073.6 | yes |
| Dunmarsh load | 1,660 | 1,664.9 | yes (on a rounding edge) |
| Corriden load | 3,570 | 3,568.2 | yes |
| Tamsell load | 3,010 | 3,011.3 | yes |
| Excess over allocation, Kestle / Hessick / Varrow | 2,540 / 1,250 / 1,120 | 2,537 / 1,246 / 1,124 | yes |
| Ambrey / Orrinwood excess | 350 / 210 | 352 / 214 | yes |
| Kestle full-record range | 2,170 to 2,630 over; 16,450 to 16,910 | 2,169 to 2,633; 16,449 to 16,913 | yes |
| Hessick range | 1,150 to 1,270; 6,810 to 6,930 | 1,146 to 1,270; 6,806 to 6,930 | yes |
| Varrow range | 1,120 to 1,210; 4,360 to 4,450 | 1,119 to 1,213; 4,359 to 4,453 | yes |
| Smearing factor range | 1.032 to 1.053 | 1.032 to 1.053 | yes |
| Rating slopes | 0.31 to 0.86 | 0.31 to 0.86 | yes |
| Top-decile load share | 34 to 63% | 34.4 to 63.0% | yes |
| Interpolation funds | Ambrey, Orrinwood, Varrow | +308, +283, +266 (Kestle -4,156, Hessick -1,067) | yes |
| DMR upstream P, kg (latest submission per month, outfall upstream of station incl. joining streams, Ambrey outfall 002 downstream) | 90, 1,040, 350, 290, 520, 1,080, 150, 340, 240, 510 | 87.7, 1,038.6, 348.8, 289.2, 521.2, 1,082.2, 152.1, 338.6, 238.8, 507.1 | yes, all ten |
| Cover crop acres (latest amendment, crop year 2026, field-share split) | 520, 1,050, 750, 840, 780, 1,100, 490, 1,070, 510, 660 | 522.7, 1,048.6, 747.3, 842.0, 778.1, 1,102.6, 489.8, 1,072.9, 511.2, 657.1 | yes, all ten |

### Evidence and forks

- Main call forced: Kestle, Hessick, Varrow in every rating-curve variant; fourth place (Ambrey) clears by about 3x less. Section 3.1 gives three funded, all three exceed allocation, so the "fewer than three" clause is not triggered.
- Fork 1 (method; main call and Q2). Interpolation funds Ambrey/Orrinwood/Varrow. Mean-concentration x total flow gives only Orrinwood (+89) and Varrow (+115) over allocation. Flow-weighted mean gives Ambrey +2,663, Orrinwood +1,961, Varrow +696. Agreement 1.4 and the prompt name no estimator. Resolved by data (leave-one-out error, storm undersampling shown by the monitoring doc's "whatever the weather" fixed schedule plus 4 to 15% of samples in the top-discharge decile), so I accept it as a method the data forces, but it is not literal-filed. Residual risk: a reviewer who demands the estimator be filed would call this underspecified_objective.
- Fork 2 (Q2 rounding to 10 kg). Unrounded loads sit within about 1 kg of a rounding edge for Pellow (735.3), Dunmarsh (1,664.9), Hessick (6,906.3, 6,905.5 with a 366-day sine period) and Kestle (16,817.5). Local versus UTC day alone moves Kestle by 390 kg, and seasonal terms by 370 kg. So the 10 kg load figures are not determinate across valid implementations; the golden's own full-record ranges show this. Acceptable only if graded as ranges or within tolerance.
- Fork 3 (Q6). `farm_practice_contracts_2024-2027.csv` carries a `watershed` column per contract; `practice_field_watershed_acres.csv` splits 26 fields across two watersheds. They disagree for about 20% of contract rows. Whole-contract label gives Kestle 1,170, Hessick 1,180, Pellow 315, Orrinwood 600; field-share split (golden) gives 1,050, 1,100, 490, 750. Agreement 4.1(b) says "contracts in its watershed" and no shipped document explains the share file. The split is the more defensible reading (the share file exists to be used), but the text does not force it. Original-vs-amended is not a real fork (the amended row is the contract in force).
- Q5 forks closed by the register (outfall river km versus station km; joining-stream join km; Ambrey outfall 002 at 0.8 km is below the 2.2 km station; Dunmarsh outfall 0.8 km below the 1.5 km station; West Branch Creamery counted via the 7.2 km join; in-service dates all consistent) and by agreement 4.1(a) (monthly average x days, latest submission, lb/d converted).
- Minor data note: approved unit values for 8 March 2026 (04:00 to 04:45 UTC) are duplicated with different values and 2 November 2025 04:00 to 04:45 UTC is missing, in all ten gages. Deduplicating either way changes no load by 0.1 kg; no effect.
- Gage rating shifts at 01-4420 and 01-4480 from 1 August 2026 are already in the approved file; the superseded provisional file is a distractor; weather and lake files are distractors.

### Files/Hygiene

**PASS.** 13 files, formats: csv (8), xlsx (2), docx, pdf, txt. One file with 350,400 rows, one with 88,320, one with 5,297, plus an 11.5 MB approved discharge file. Real-looking operational artifacts (WQX-style export with EDT/EST, DMR-style export, Merrifield transmittal, register). Provenance and fiction clean; no authoring language seen. Temporal coherence fine (results to 23 Sep 2026, transmittal 14 Dec 2026, export 8 Jan 2027, January committee). Distractors: provisional discharge file, weather precipitation, lake summer monitoring. Not public canonical data. No exclusion-level finding.

### Stump power

Moderate to strong. The easy route (interpolate or average the grab samples, which is also what a plain reading of 1.4 suggests) funds Ambrey, Orrinwood and Varrow, so a solver who does not model concentration against discharge gets two of three wrong. Because dry-weather fixed-schedule sampling is described in the monitoring doc and the storm samples are sparse, a careful solver can see the bias; GPT-class solvers that run any rating curve will pass the main call, so the stump is selective rather than guaranteed. Not too easy: no shipped document names the trap.

### Stumping type

`mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. All reported data are honest; the trap is estimator choice (rating curve with retransformation versus interpolation) pinned by out-of-sample behaviour. Passes Gate G.

### Three rules

`domain: pass`, `layers: pass`, `decisive_step: analytical`. The field's own work is estimating annual tributary phosphorus loads from sparse grab samples and continuous discharge (concentration-discharge rating curve, seasonal terms, retransformation bias); the swap test fails to preserve meaning (hospital or megawatt-hours cannot replace it). Layer 1: ug/L versus mg/L and renamed parameter, ACWL versus BLC station ids, UTC unit values versus local daily means, provisional versus approved discharge, a gage 4.2 km above the Dunmarsh station needing an area ratio, DMR resubmissions and mixed lb/d versus mg/L, contract amendments. Layer 2: unbiased load estimation on a flow-biased sample, where the easy route (interpolate or average samples across days) gives Ambrey, Orrinwood and Varrow, the wrong three.

### Fix

- prompt: add to the cover crop ask a pin such as "apportion each field's contracted acres among the watersheds by the shares in practice_field_watershed_acres.csv", or relabel the contracts column so it does not read as an authoritative watershed (supplementary Q6).
- solution/rubric: grade the Q2 loads as ranges or with tolerance wider than 10 kg and keep the existing full-record ranges; do not require the exact 10 kg values.
- Optional hardening of determinism without moving the stump: none needed for the main call.

### Repairs after pass 1 (one generator pass)

- The cover crop acres: agreement 4.1(b) counts the acres lying in each watershed on fields under contract; the ask's devices were rebuilt (the contract export repeats a contract's acres on each enrolled field's line, the overlay gives each field's own acres and shares), and the export's header states that contracts enrol whole fields and that the latest amendment is the contract in force.
- The wastewater phosphorus: the smaller dischargers report by calendar quarter, each report stating its monitoring period; the register states its river-km datum.
- The loads: given as ranges over the full-record rating curves, rounded outward to 10 kg, in the memo and in the write-up.
- The 15-minute record: continuous in UTC through both clock changes.
- Unchanged: the call, the ladder and every main-call figure (figures.json compared before and after).

## Pass 2 (2026-10-13), the one re-judge, on the repaired cut


- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE. No repair is required. Two optional notes sit under Evidence: the load ranges in supplementary answer 2 reproduce to within 10 kg at the edges only, and the estimation method is not filed. Neither needs a rerun.
- **Why:** The funded set {Kestle River, Hessick River, Varrow Brook} reproduces from the bundle under the rating-curve family of load methods (plain, seasonal, quadratic, normal-theory or smearing retransformation, composite, ratio estimator on the full record) and under every cleaning variant I tried. The gap from third place (Varrow Brook, +1,110 to +1,220 kg) to fourth (Ambrey River, +340 to +370 kg) is large and clean. The one competing answer, linear interpolation of the samples, funds Ambrey River, Orrinwood Brook and Varrow Brook. The data rule it out: in leave-one-out validation, the absolute load error is 28 to 77 per cent of observed load for interpolation against 17 to 39 per cent for the rating curve, and on the highest-flow fifth of sample days interpolation misses 18 to 81 per cent against 15 to 45 per cent (at Kestle River and Hessick River, 81 and 79 per cent against 19 and 15). The strongest remaining critique is that no file names the method (agreement 1.4 says only "estimated from the tributary monitoring record"), but the data separate the candidates.

### Evidence (recomputation ledger)

Method: total P (fraction Total), routine and Accepted, ug/L converted to mg/L, BLC plus ACWL stations mapped through the register (79 to 81 samples per station, which reproduced). Local-day means were built from the UTC 15-minute approved values. Daily-value files were used for WY24 and WY25. Dunmarsh Brook was scaled by 61.4/52.8. Fit: ln C on ln Q plus sine and cosine of day of year, with smearing. Loads in kg, excess = load minus Schedule 1 allocation.

| Figure | Claimed | Recomputed | Reproduced |
|---|---|---|---|
| Kestle River load, seasonal | 16,820 | 16,818 | yes |
| Hessick River load | 6,910 | 6,906 | yes |
| Varrow Brook load | 4,360 | 4,364 | yes |
| Ambrey River load | 3,730 | 3,732 | yes |
| Orrinwood Brook load | 2,600 | 2,604 | yes |
| Pellow Brook load | 740 | 735 | yes |
| Fallowmere Brook load | 1,070 | 1,074 | yes |
| Dunmarsh Brook load | 1,660 | 1,665 | yes |
| Corriden River load | 3,570 | 3,568 | yes |
| Tamsell River load | 3,010 | 3,011 | yes |
| Excess, Kestle River (3.1) | 2,540 | 2,538 | yes |
| Excess, Hessick River | 1,250 | 1,246 | yes |
| Excess, Varrow Brook | 1,120 | 1,124 | yes |
| Excess, Ambrey River | 350 | 352 | yes |
| Excess, Orrinwood Brook | 210 | 214 | yes |
| Excess range, Kestle River | 2,160 to 2,640 | 2,169 (plain) to 2,633 (normal-theory) | yes |
| Excess range, Hessick River | 1,140 to 1,270 | 1,146 to 1,267 | yes |
| Excess range, Varrow Brook | 1,110 to 1,220 | 1,119 to 1,225 (quadratic, normal-theory) | within 10 kg |
| Excess range, Ambrey River | 340 to 370 | 344 to 368 (quadratic, normal-theory 374) | within 10 kg |
| Excess range, Orrinwood Brook | 210 to 230 | 214 to 221 (up to 225 for the quadratic variant) | yes |
| Interpolation excess, Kestle River | -4,160 | -4,156 | yes |
| Interpolation excess, Hessick River | -1,060 | -1,067 | yes |
| Interpolation funds | Ambrey River, Orrinwood Brook, Varrow Brook | Ambrey River +308, Orrinwood Brook +283, Varrow Brook +266 | yes |
| Smearing factor | 1.032 to 1.053 | 1.032 to 1.053 | yes |
| Rating slopes | 0.31 to 0.86 | 0.30 to 0.86 | yes |
| Top-decile days' load share | 34 to 63% | 34 to 62% | yes |
| Top-decile days' sample share | 4 to 15% | 3.8 to 15.4% (WY2026 samples; 9 to 20% if all 79 to 81 samples are counted) | yes, the base is unstated |
| Upstream P, Fallowmere Brook | 80 | 81.2 | yes |
| Upstream P, Kestle River | 1,040 | 1,037.7 | yes |
| Upstream P, Orrinwood Brook | 340 | 337.3 | yes |
| Upstream P, Tamsell River | 310 | 312.2 | yes |
| Upstream P, Varrow Brook | 480 | 477.3 | yes |
| Upstream P, Hessick River | 1,050 | 1,047.0 | yes |
| Upstream P, Pellow Brook | 170 | 172.1 | yes |
| Upstream P, Ambrey River | 320 | 322.7 | yes |
| Upstream P, Dunmarsh Brook | 280 | 278.4 | yes |
| Upstream P, Corriden River | 540 | 542.6 | yes |
| Cover crop acres, Fallowmere Brook | 630 | 632.6 | yes |
| Cover crop acres, Kestle River | 1,030 | 1,029.7 | yes |
| Cover crop acres, Orrinwood Brook | 1,040 | 1,038.7 | yes |
| Cover crop acres, Tamsell River | 690 | 687.0 | yes |
| Cover crop acres, Varrow Brook | 900 | 898.4 | yes |
| Cover crop acres, Hessick River | 1,500 | 1,501.4 | yes |
| Cover crop acres, Pellow Brook | 660 | 657.7 | yes |
| Cover crop acres, Ambrey River | 1,180 | 1,182.2 | yes |
| Cover crop acres, Dunmarsh Brook | 840 | 837.6 | yes |
| Cover crop acres, Corriden River | 750 | 751.3 | yes |

Sources for the upstream P and acre rows:
- Upstream P: `npdes_dmr_phosphorus_wy2026.csv` at the latest received resubmission (21 resubmission rows). Quarterly reports use the days of the quarter and lb/d is converted to kg. The Streams and Facilities sheets of `blc_station_register.xlsx` decide which outfalls count.
- Outfalls excluded as downstream of the station: Ambrey outfall 002 (km 0.8 below the km 2.2 station) and Dunmarsh Wastewater Treatment Facility (km 0.8 below the km 1.5 station).
- Ambrey outfall 001 counts for its Oct to Mar reports only.
- Acres: `farm_practice_contracts_2024-2027.csv` (latest amendment, crop year 2026, 97 contracts, 172 fields, contracted_acres equal to the field sum) joined to `practice_field_watershed_acres.csv` shares.
- Every upstream-P and acre figure sits 2 or more units from a round-to-10 boundary.

Findings that do not change the verdict:
- **Edge ranges, supplementary answer 2.** Upper edges (Ambrey River 3,750, Varrow Brook 4,460) depend on the day-of-year period and the normal-theory variance degrees of freedom. My variants reach 3,753 and 4,465. Point loads and the call are unaffected, and a grader tolerance of 10 kg covers it.
- **Load figure to 10 kg.** The prompt says "round kilograms to the nearest 10", yet a load figure carries about ±1.5 per cent method freedom (Kestle River spread 480 kg). The golden answers with ranges, so the point values are tolerance-graded rather than literal. Treat this as a rubric note, not a determinism defect.

Robustness of the funded set, with the top three by excess in each variant:

| Variant | Top three | Same set? |
|---|---|---|
| Seasonal, plain, quadratic, normal-theory | Kestle River, Hessick River, Varrow Brook | yes |
| WY26 samples only | Kestle River, Hessick River, Varrow Brook | yes |
| WY25 and WY26 samples | Kestle River, Varrow Brook, Hessick River | yes (order changes) |
| BLC samples only | Kestle River, Hessick River, Varrow Brook | yes |
| Composite (rating curve plus interpolated residual) | Kestle River, Hessick River, Varrow Brook | yes |
| Provisional Jul to Sep file used by mistake | Kestle River, Hessick River, Varrow Brook | yes |
| Ratio estimator, full record | Kestle River, Hessick River, Varrow Brook | yes |
| Interpolation of concentration (all samples, WY26 samples) | Ambrey River, Orrinwood Brook, Varrow Brook | no |
| Interpolation of instantaneous load | Ambrey River, Orrinwood Brook, Varrow Brook | no |
| Mean concentration times flow, all samples | Varrow Brook, Ambrey River, Pellow Brook | no |
| Mean concentration times flow, WY26 samples | Varrow Brook, Orrinwood Brook, Ambrey River | no |
| Ratio estimator, WY26 samples | Ambrey River, Orrinwood Brook, Varrow Brook | no |
| ACWL samples only | Kestle River, Corriden River, Hessick River | no |

The failing variants either ignore the concentration-discharge relationship the record shows (slopes 0.31 to 0.86) or use a small subset. Dropping the retransformation correction lowers every excess (Kestle River +1,711) but keeps the same three; it falls outside the filed ranges.

Fork between rating curve and interpolation, explicitly:
- Rating curve (seasonal): Kestle River +2,538, Hessick River +1,246, Varrow Brook +1,124, so it funds Kestle River, Hessick River and Varrow Brook.
- Linear interpolation of sampled concentration across days: Kestle River -4,156, Hessick River -1,067, Ambrey River +308, Orrinwood Brook +283, Varrow Brook +266, so it funds Ambrey River, Orrinwood Brook and Varrow Brook.
- The data separate the two. Leave-one-out load error is 17 to 39 per cent for the rating curve against 28 to 77 per cent for interpolation. At the highest-flow 20 per cent of sample days, interpolation recovers only 19 to 21 per cent of the true load at Kestle River and Hessick River (bias ratio 0.19 and 0.21), where the rating curve recovers 92 and 98 per cent.
- Residual risk (Gate C, low to moderate): agreement 1.4 and the prompt never name the method. A solver who interpolates reproduces every number correctly and diverges, and that fork is only closed by validation, not by a filed sentence.

Other forks checked and closed by the files:
- UTC against local day: closed by the transmittal.
- Superseded provisional file: closed by the transmittal and the file header.
- ug/L against mg/L: closed by the unit column.
- Rejected, replicate and blank rows: closed by the status and activity-type columns.
- Dunmarsh Brook gage-to-station area scaling: closed by the register.
- Facility upstream test: closed by Streams and Facilities river km.
- Resubmissions: closed by `RECEIVED_DATE` and `SUBMISSION_TYPE`.
- Amendments: closed by the contract file header.

### Files/Hygiene: PASS

- 13 files and 5 formats: csv, xlsx, pdf, docx, txt. `merrifield_unit_values_wy2026_approved.csv` has 350,400 rows, which satisfies the 25,000-row gate.
- Distractors: the provisional unit values, `lake_brannoch_summer_monitoring_2024-2026.xlsx`, `blc_weather_precipitation_wy2024-wy2026.csv`, and the other crop-year contract rows. None is named by trap in a file name.
- Realism: the exports carry real-system irregularities (EDT and EST stamps, comment lines in headers, QC rows, rejected rows, lab-reporting switch). No tool banners or authoring language found.
- Temporal coherence is fine (WQ export 2027-01-08, transmittal 2026-12-14, contracts exported 2027-01-08).
- No exclusion-level findings.
- Mild observation: the monitoring-program docx explains the sampling design ("whatever the weather", storm samples "during high water") in prose. It gives context only and no answer.

### Stump power (Gate F)

Moderate to good. The trap that will do the work is the load estimator. Linear interpolation or mean-concentration times flow is the easy route, and it gives a 3-tributary slate with 2 wrong picks, and the Kestle River under its allocation by 4,160 kg. A strong model that builds a rating curve and checks it against interpolation will pass. The supplementary asks (upstream P with the Ambrey outfall change, the downstream Dunmarsh outfall, resubmissions, quarterly reports, lb/d, and fractional-field acres under amended contracts) carry the remaining difficulty and are hard to complete correctly. Too-easy signals are limited: nothing in the pack ranks candidates or pre-computes a load.

### Stumping type (Gate G)

`mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported numbers are fine (no shipped load figure is wrong). The difficulty is choosing the load estimator that the data's concentration-discharge structure and high-flow undersampling support, and it survives on clean data. Passes Gate G.

### Three rules (Gate H)

`domain: pass`, `layers: pass`, `decisive_step: analytical`.

- **Domain.** Swap test: replacing "phosphorus load" with "visits" would remove the whole method choice. Tributary nutrient load estimation from sparse grab samples and a continuous gage record is core water-quality and hydrology work.
- **Layer 1.** UTC unit values against local-day dailies, a provisional and an approved release, two sample providers with different units and names, a change of laboratory, quarterly against monthly DMR reports, lb/d against mg/L with MGD, resubmissions, an outfall moved downstream of the station, and a gage-to-station area ratio.
- **Layer 2.** Estimating load from sparse samples with a rating curve that the validation and the sampling structure support, against interpolation between sampling days.
- **Easy route.** A strong analyst who cleaned everything and read every rule correctly could still interpolate sampled concentration between sampling days and multiply by daily flow, or average concentrations. That produces an Ambrey River, Orrinwood Brook and Varrow Brook slate with Kestle River 4,160 kg under.
- Rule 3 does not bind the asks. The upstream P and acre figures are rule application, which is allowed for supplementary asks.

### Fix

none. Optional hygiene of the answer key: in the supplementary-2 ranges, either widen the upper edges by 10 kg or state the variance degrees of freedom and the day-of-year period; state the sample base for the "4 to 15 per cent" figure (WY2026 samples).

### After pass 2

- APPROVE. Its two optional notes were applied to the answer key only: the load ranges in the write-up carry 10 kg of tolerance at each end, and the 4 to 15 per cent sample share is stated on water year 2026's samples. No file under target/ changed.
