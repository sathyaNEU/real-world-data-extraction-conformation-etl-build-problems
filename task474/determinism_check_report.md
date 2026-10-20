# Determinism verdict, task474 (round 1)

- **Verdict:** DETERMINISTIC (no SOLUTION_WRONG). Every figure in FINAL_RECOMMENDATION, SUPPLEMENTARY_ANSWERS and CRITICAL_COMPONENTS reproduced from the bundle.
- **Disposition:** APPROVE. Two optional one-line layout pins are listed under Fix. Neither moves a figure, so no rerun is needed.
- **Why:** Rule 2.2 asks for each town's residents in poverty "in that year". No file publishes that figure: the methods note says the SDC does not publish town estimates, and the ACS B17001 town count is a 60-month period estimate. Only the calibrated estimator (SNAP recipients that year x the town's ACS count / its 2020-2024 mean recipients) is both residents-in-poverty in level and year-specific, and the ratio window matches the ACS window. Run literally, it gives the golden nine amounts. The ACS-only and recipients-only routes each fail one half of the rule's wording. They give different amounts: ACS-only changes 6 of 9 rounded amounts and recipients-only changes 9 of 9, as shown below.

## Literal reading and recomputed values

**Inputs.**
- County estimates as last published: 2020 from Dec 2022 Table 2, 2021 from Dec 2023 Table 2, 2022 from Dec 2024 Table 2. The county totals are 237,551, 240,214 and 241,527, and they reproduced.
- Regions: 2023 revised from the xlsx Table 2 and 2024 first from the xlsx Table 1.

**Town joins.**
- All 118 DSS town names match the codes file once the 7 abbreviations are mapped: E ORMSBY, W CORWIN, N WEXPORT, LWR SAXSTEAD, UPR DRAYBURY, PENNOCK CTR and LARKSPUR-HILL.
- The ACS ratio (B17001_002 over each town's 2020-2024 mean recipients) runs from 0.865 to 3.128, matching the stated 0.87 to 3.13.

**Residents in poverty (ask 1).** Rounded to the nearest hundred, all 36 year figures and all 9 averages match.

| Region | 2020 | 2021 | 2022 | Avg 2020-24 |
|---|---|---|---|---|
| Greater Ormsby | 35,868 | 34,319 | 31,591 | 33,089 |
| Mill River Valley | 41,592 | 44,019 | 46,845 | 45,102 |
| Tarrow Uplands | 6,717 | 6,741 | 6,669 | 6,604 |
| Southern Shore | 12,585 | 13,263 | 14,581 | 14,483 |
| Wexport Harbor | 43,983 | 44,008 | 42,837 | 42,874 |
| Two Rivers | 35,777 | 36,682 | 37,886 | 37,394 |
| Northern Hills | 6,815 | 6,710 | 6,713 | 6,682 |
| Quinnet Valley | 27,611 | 27,592 | 27,366 | 27,640 |
| Eastern Bays | 26,604 | 26,880 | 27,040 | 26,909 |

The nine averages sum to 240,776. The nine rounded averages sum to 240,800, as claimed.

**Allocations (rule 2.4).** The unrounded values are 1,649,112; 2,247,829; 329,117; 721,813; 2,136,812; 1,863,665; 333,014; 1,377,534 and 1,341,104. Rounded to $10,000 they equal the golden nine amounts, which sum to $12,000,000. The closest rounding boundaries are Two Rivers (1,335 away), Wexport Harbor (1,812) and Northern Hills (1,986).

**Robustness within the calibrated estimator.** None of these moves a single rounded amount or a single hundred-rounded residents figure:
- households instead of recipients;
- first rather than revised 2023;
- rounded recipients;
- the ratio to the unrounded mean.

**Transition asks (3 to 5).**
- The window is service_date July 1, 2025 to June 30, 2026.
- The CCA old numbers are mapped through the conversion file.
- The town at the service date is old_value if service_date is before effective_date, otherwise new_value.
- People are counted distinct per agency, region and person.
- EA is counted once per household_no and service_date. All 4,873 household-dates have identical amounts across members, the same agency and the same town.
- Unexpended balances are award minus expended, and every figure agrees.
- Ask 3 balances total $549,981, matching the golden.
- Ask 4 people and ask 5 EA match the golden.
- All 36 figures across asks 3, 4 and 5 match (balances, people and EA).
- The 1,255 exact duplicate rows (1,176 of them the Wexmoor April 2026 upload) cannot move any figure. People are distinct counts and EA collapses by household-date.

## Competing answers and forks (Gate C)

1. **Town weights for 2020-2022 (main call, asks 1 and 2). Mild residual fork.** The prompt and rule do not name the town proxy.

   | Reading | Greater Ormsby | Amounts that differ |
   |---|---|---|
   | Calibrated, golden | $1,650,000 | none |
   | ACS 5-year shares | $1,620,000 | 6 of 9 |
   | Recipients only | $1,750,000 | 9 of 9 |
   | Calibrated to 2022 recipients | $1,680,000 | 4 of 9 |
   | Calibrated with elasticity 0.5 / 0.75 / 1.25 | $1,633,000 / $1,642,000 / $1,656,000 | 6 / 5 / 2 |

   Why the golden is forced:
   - Rule 2.2 says "in that year", which excludes ACS-only. The ACS notes state the count describes the 60 months January 2020 to December 2024. Applying the same share to all three years would also make the regional 2020-2022 figures flat, which contradicts the year-specific SNAP movement.
   - "Residents in poverty" excludes recipients-only. The methods note defines the quantity as residents below the threshold, and the survey count differs from recipients by 0.87 to 3.13 times.
   - Calibration over the ACS window is the only temporally consistent one.
   - Proportionality (elasticity 1) is the natural reading of "proportion".

   Back-test: I allocated the 2023 and 2024 State totals by each weight and compared against the published regions. The golden has the lowest RMSE (about 1,080 and 1,020, against about 1,320 and 1,240 for ACS-only and about 2,380 and 2,340 for recipients-only). The margin over ACS-only is modest and inside the SDC 90% interval half-widths, so the data separate the candidates only weakly. The wording and period logic carry the decision, not the back-test. I score this as pass with residual risk: no shipped file states the proxy, and an ACS-only solver can cite the survey's own "period estimate" note without being irrational.

2. **Tie-day on effective_date (35 rows). Low risk.** The layout says effective_date is "the date the change took effect". Reading "took effect on D" as new town from D gives the golden. The alternative, old town through D, changes graded figures:

   | Ask | Golden | Alternative |
   |---|---|---|
   | 4, Greater Ormsby people | 4,080 | 4,084 |
   | 4, Mill River Valley people | 5,677 | 5,672 |
   | 4, Southern Shore people | 2,126 | 2,123 |
   | 4, Wexport Harbor people | 5,210 | 5,213 |
   | 3, Mill River Valley balance | $98,700 | $98,600 |
   | 3, Wexport Harbor balance | $93,200 | $93,300 |
   | 5, Greater Ormsby EA | $505,600 | $507,400 |
   | 5, Mill River Valley EA | $679,700 | $678,000 |
   | 5, Wexport Harbor EA | $644,800 | $643,700 |
   | 5, Quinnet Valley EA | $487,100 | $488,200 |

   The literal text favours the golden. The inclusive reading is not licensed, so the golden stands.

3. **Row town versus audit trail. Closed by the files.** For every non-CCA row, the extract town equals the audit's new_value, so it is the town as of the cut. For CCA, rows under old numbers keep the old town. The rule says "while they lived" and "when they were paid", and the audit trail with effective_date is shipped. Using the row town and the old and new CCA numbers separately gives very different counts: 3,841 against 4,080 for Greater Ormsby. That is a competent-solver path to a wrong ask answer, not a fork.

4. **EA once per household-date. Inferred but forced.** The layout does not say the EA amount repeats per member. The rule's unit is "households", and the amounts are identical across members in all 4,873 groups. Summing raw rows gives about 2.3 times the figure.

5. **"Served" includes NS.** Every service code is a "service delivered" in the layout. Excluding NS would change the counts to 3,871; 5,357; 746; 2,021; 5,040; 4,799; 879; 3,726; 3,079. That is not licensed by any text.

6. **Margin test.** The nine allocation margins to the rounding boundary are $1.3k to $4.1k on a $12M base. Within the calibrated family they are insensitive. Only an elasticity change or a different proxy crosses them (fork 1).

Gates A, B, D and E pass. Every decisive fact is in a shipped file: the rule PDF, the SDC PDFs and xlsx, DSS, ACS, the codes file, the closeout, and the extract, audit and conversion files. The vocabulary is present too: "as last published", "while they lived", "when they were paid". The CSV column layout is unspecified, but the graded values are fixed. The asks give units and rounding in the sentence.

## Files/Hygiene: PASS

- 18 files in csv, txt, pdf and xlsx (4 formats). The extract has 89,023 rows.
- Distractors: the 2020 area-crosswalk factors, the Dec 2021 release, the FY2026 allocation table and the ACS 5-year town shares.
- No authoring disclosures found. Dates are coherent: rule September 15, 2026; closeout October 2; extract September 30; audit effective dates up to 2026-05-26.
- ACS table notes are real Census-style text, and the SDC PDFs and workbooks read as real.
- No exclusion-level finding.

## Stump power (Gate F)

Two natural easy routes give specific wrong answers: ACS 5-year town shares (Greater Ormsby $1,620,000) and SNAP recipient shares ($1,750,000). A solver who also does not notice the ACS period mismatch fails. A solver who notices it must still choose the ratio window and form, and the ratio-to-2022 shortcut gives yet another wrong set. The asks add the audit trail, the CCA conversion and household-level EA as independent fail points. Stump power is plausible. The weakness is that the ACS-only route is not irrational (fork 1), so some failures there would be interpretive rather than analytical.

## Stumping type (Gate G)

`mechanism: method_or_model_selection` (with etl_conformance in the asks), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.

The county estimates, the ACS counts and the SNAP series are all correct as reported. The difficulty is aligning a period estimate with a calendar-year estimand and calibrating a year-specific indicator to it, not rejecting a misleading number. On clean data the same temporal-alignment problem remains.

## Three rules (Gate H)

`domain: pass`, `layers: pass`, `decisive_step: analytical`.

- **H1.** The deciding quantity is a demographer's downscaling of model-based county poverty estimates to a new geography with a year-specific administrative proxy calibrated to a period survey. Swapping "hospital" for "school" changes nothing about the problem, but it is not a stated score or an eligibility list. It is the field's own estimation work.
- **H2.** Layer 1: PDF and xlsx layouts across vintages, preliminary and revised releases, county-to-region geography change, abbreviated DSS town names, CCA client renumbering, a duplicated upload, an as-of-cut town field and a repeated household EA amount. Layer 2: aligning the 60-month ACS count to calendar-year weights.
- **H3.** The easy route is to use the ACS town counts directly as the shares for all three years, or to use recipients as the shares. A strong analyst who read every rule and field correctly still files Greater Ormsby $1,620,000 or $1,750,000. The decisive step is choosing the estimand's reference period and level, which is analysis, not semantics or rule application.

## Fix (optional, none required)

- **Where:** input_files, layout text only. This pins counting and changes no figure.
- **Pin 1:** in `rof_gds_export_layout.txt`, say that effective_date is the first date the new value applies.
- **Pin 2:** in the same file, say that the EA amount is the household's payment and is repeated on each member's row.
- **Rerun:** no rerun is needed, since solvers' data and figures are unchanged.
