# task194 determinism review (isolated judge)

File universe: fresh unzip at `/tmp/claude-0/-home-user/5ec7cb86-793f-5895-a00b-808e36976e12/scratchpad/task194_judge_pack/`
(21 members). Nothing under the repo task folder was opened except this report, which is overwritten here.
Every figure below was recomputed from the shipped files with pandas; no arithmetic was taken on trust.

## Part 0: the answer the prompt and the bundle lead to, before the graded blocks were opened

Enumeration written first, from the prompt, the two PDFs and the data only.

1. **Eligible set.** Charter 4.2 (`improvement_partnership_charter_v3.pdf`): acute inpatient units still reporting
   under their own cost centre at the decision date, 4+ closed quarters under spec 4.0, minus any unit placed with
   in the previous twelve closed quarters, minus the unit the team is with when the decision is made. Decision date
   is the March committee, 24 March 2027 (charter 4.1 + `placement_cycle_notes.txt`, 24 Feb note). Last closed quarter
   is 2026-27 Q2, so the twelve-quarter window is 2023-24 Q3 to 2026-27 Q2, which covers IP-01 to IP-09; IP-10 (41460)
   is the current placement. Service type from `unit_register.csv` drops 41610/41620/41630; closure drops 41511/41512.
   **Result: 12 units** - 41210, 41220, 41230, 41240, 41310, 41320, 41330, 41410, 41420, 41430, 41510, 41520.
2. **Avoidable complications.** Charter 4.3: observed complications of the unit's own patients less the expected
   complications of its episodes, under spec 4.0. Spec 2.2/2.3 fix the denominator (care type Acute, LOS >= 1,
   acute-inpatient unit, DRG mapped to a band); spec 3.1 and Appendix A fix expected.
   I rebuilt all 215 unit-quarters of `unit_indicator_series.csv` from `episode_outcomes_extract.csv` +
   `drg_risk_bands.csv` + `hac_stratum_rates.csv` after de-duplicating on the dictionary's own separation key
   (unit, patient, admission date, DRG; 1,546 duplicate rows in the extract). **Every in-scope episode count,
   observed count and expected value reproduced exactly** (0 mismatches on 215 rows).
3. **The structure that decides it.** `coding_close_out_register.csv` is a development triangle: each quarter is
   published at its coding close and restated at every close after. For 41210, 2024-25 Q1 runs 185, 243, 287, 322,
   334 and then holds; for 41220 the same quarter runs 335 to 346. Charter 4.3 asks for "the complications its own
   patients had", not the complications coded so far, so the open quarters must be carried to ultimate. Five of the
   ten closed quarters for 41210 have not settled (2025-26 Q2, Q3, Q4; 2026-27 Q1, Q2).
4. **Development basis.** Age-to-ultimate factors from each unit's own settled quarters. The register itself forbids
   pooling: age-1 ultimate/first ratios are 1.719-1.805 for 41210 and 1.018-1.054 for 41220, i.e. the between-unit
   spread dwarfs the within-unit spread. `unit_register.cis_registered_date` supplies the mechanism and is almost
   monotone in the factor (41310 2022-07-01 -> 1.047 ... 41450 2025-10-01 -> 1.858, 41520 2027-01-04 -> 1.716,
   41210 2027-03-01 -> 1.763). The denominators are not censored: the in-scope/separations ratio for 41210 is
   0.900-0.917 in every quarter including the most recent, so only the numerator develops.
5. **Forward basis.** Charter 4.4 and spec 3.4: planned separations for the assessment quarter from
   `activity_plan_2027q4.csv` times the unit's rate per separation over the specification period to date, with
   "separations" the all-care-type count the dictionary defines and `activity_summary_monthly.csv` publishes.
6. **My answer, reached before reading the blocks: Alderbrook General Medicine, cost centre 41210, 44.6 avoidable
   complications on 4,261 planned separations, next unit 41220 at 27.8.** The easy route (rank on the series as
   reported) gives 41220 at 26.1; the dashboard route makes 41210 look like the best unit in the network (SR 0.738).

## Verdict

- **Verdict: DETERMINISTIC + SOLUTION_WRONG**
- **Disposition: FIX_NOW.** Regenerate Critical Component 1 / Solution Step 3 (the "4 of the 10" count is wrong),
  drop or correct the ungrounded cycle label "IP-11", and fix two inverted sentences. No input file changes, no
  graded figure moves, **no model rerun required**.
- **Taxonomy: solution_incorrect** (block-level only; the decision is forced). **Fix location: solution.**

**Why.** The call is forced. Every load-bearing figure reproduced to the stated rounding, all 12 unit values and the
gap included, and the one method fork that flips the winner (pooled rather than own-unit development factors) is
refuted twice by the shipped data, so no competing answer survives. What fails is the write-up: Critical Component 1
names four unsettled quarters when its own stated test ("a quarter whose last two publications agree has settled")
makes five of the ten unsettled, and the omitted quarter carries most of the uplift the recommendation rests on.

## Gate table

| Gate | Line |
|---|---|
| A - solution correct | **PASS with SOLUTION_WRONG.** All 215 unit-quarters of the indicator series rebuilt exactly from the extract; 3097, 3023.6, 3408.5, 311.5, 1.763, 1.0368, 44.6, 27.8, 16.8, 1.604, 26.1, 27.59, "5 of 12" and all three supplementary tables reproduced. Defects: Critical Component 1 / Step 3 miscount the unsettled quarters; three inverted or ungrounded sentences (below). |
| B - decisive facts shipped | **PASS.** Eligibility charter 4.2; avoidable charter 4.3; forward basis charter 4.4 + spec 3.4 + `activity_plan_2027q4.csv`; denominator spec 2.2/2.3 + `drg_risk_bands.csv` + `unit_register.service_type`; rates spec App. A + `hac_stratum_rates.csv`; censoring `coding_close_out_register.csv` + spec 3.7 + `placement_cycle_notes.txt` (19 Feb note on the coding queue); unit-specific lag `unit_register.cis_registered_date`; site-by-month `activity_summary_monthly.facility`; revision map `hac_category_list.csv` + spec App. B; the detail extract's campus omission `export_manifest.csv`. One vocabulary miss: "cycle IP-11" is in no shipped file (grep returns zero hits). |
| C - uniquely forced | **PASS.** Eight development variants tested; all name 41210 (ratio 1.530 to 1.628). The only flip is pooled factors, refuted by the register's own between-unit spread and the CIS-rollout gradient. The per-separation denominator fork moves the printed values but not the ranking. 41210 also wins with the eligibility filter removed entirely (44.61 against 36.24 for the next unit), so no eligibility misreading can flip it. |
| D - hardness not semantics | **PASS.** The split is analytical: whether the register's open quarters are carried to ultimate, and on whose pattern. Neither turns on a word's meaning. |
| E - prompt unambiguous on the decision | **PASS.** One committed unit, one gap, three supplementary tables each with period, grain, attribution ("counted to the site each unit reported under that month") and rounding pinned in the asking sentence. |
| F - stump power | **STRONG.** See below. |
| G - stumping type | **PASS** (forecasting). See the Gate G line. |
| H - the three rules | **PASS.** See the Gate H line. |

## Evidence: load-bearing values recomputed

| Claim | Recomputed | Status |
|---|---|---|
| 12 eligible units, the named 12 | 12, identical list | reproduced |
| 41210 observed 3097, expected 3023.6 | 3097, 3023.647 | reproduced |
| 41210 developed 3408.5, uplift 311.5 | 3408.55, +311.55 | reproduced |
| age-1 factor 1.763 (41210) / 1.0368 (41220) | 1.7630 / 1.0368 (volume-weighted over settled quarters) | reproduced |
| 44.6 / 27.8 / 18.5 / 14.9 / 12.9 / 11.6 / 6.9 / 6.4 / 4.9 / 4.3 / 3.2 / 1.9 | 44.61, 27.81, 18.51, 14.79, 12.91, 11.54, 6.90, 6.39, 4.87, 4.32, 3.19, 1.89 | all 12 reproduced, same order |
| gap 16.8, margin 1.604x | 16.80, 1.604 | reproduced |
| 41220 leads the record as it stands at 26.1 | 26.14 | reproduced |
| 41320 leads the last four closed quarters at 27.59 | 27.59 | reproduced |
| 41210 reads 5 of 12 on the record as it stands | 5th of 12 | reproduced |
| Supp. 1 (not measured / with complication) H1 7198/383, H2 6108/369, H3 6715/421, H4 1914/145 | identical, from published monthly separations less in-scope episodes, attributed by `facility` of the month | reproduced |
| Supp. 2 (sub-acute and mental health, 10 quarters) 1443/107 ... 1295/116 | all 20 figures identical | reproduced |
| Supp. 3 (8 groups x 2 years) G1 3563/1618 ... G8 1661/757 | all 16 figures identical, revision-aware map plus first-category fallback for the 1,026 in-scope complication episodes absent from the detail extract (41520, 41510, 41511, 41512) | reproduced |
| "4 of the ten closed quarters are still being added to" | **5 of 10** under the block's own settled test | **not reproduced** |
| "between 1.528 and 1.608 times" | 1.530 to 1.608 over eight variants; no variant yields 1.528 | **not reproduced (1.530)** |

### Forks examined and how each closes

| Fork | Answers it produces | Closure |
|---|---|---|
| Own-unit vs pooled age-to-ultimate factors | 41210 at 44.61 / **41220 at 34.41** (41210 drops to 4th at 15.95) | Closed by the data, not by inference: 41210's five own age-1 ratios are 1.719-1.805 against a pooled 1.149, and `cis_registered_date` is near-monotone in the factor across all 23 units. Pooling is a demonstrable error here, not a licensed alternative. |
| Volume-weighted vs simple average; all settled quarters vs last 4 / 3 / 2; cumulated link ratios | 44.61, 44.73, 43.46, 43.60, 43.42, 43.58, 41.88, 44.61 | All name 41210; margin 1.530 to 1.608. |
| "Per separation" = all-care-type separations (36,767) vs in-scope episodes (33,494) | 44.6 vs 49.0 (41220 27.8 vs 30.1) | Closed by text: spec 3.4 says "per separation", the spec calls the indicator denominator "episodes", and the dictionary defines `separations` as all care types, matching `planned_separations`. Ranking identical either way. Flagged as the one residual grading risk on the 12 printed values. |
| Develop the ratio rather than the count | same | The denominator is not censored (in-scope/separations 0.900-0.917 in every quarter), so there is nothing to develop. |
| Supp. 1 source: published separations less in-scope vs extract row counts less in-scope | 7198/6108/6715/1914 vs 7101/6161/6813/2014 | Closed by `export_manifest.csv`: the episode extract "omits uncoded episodes", the activity summary "omits nothing". |
| Supp. 2 source: "reported" vs recomputed from the extract | 1443 vs 1526 (de-duplicated) in 2024-25 Q1 | Closed by the word "reported" plus the dictionary's "separations the unit reported in the month" and the manifest's "as published". |
| Eligibility window readings (twelve closed quarters vs charter 4.2's three years) | same 12 | IP-01 to IP-09 fall inside every reading; 41210 wins even unfiltered. |

## Defects to repair (all in the solution blocks)

1. **Critical Component 1 and Solution Step 3 are wrong.** "Four of the ten closed quarters are still being added to
   ... 2025-26 Q2, Q3, Q4 and 2026-27 Q1" / "4 of the 10 have not". Under the block's own test, **five** of the ten
   have not settled: 2026-27 Q2 has a single publication (218) and is the quarter the pull date cuts shortest. The
   computation that produces the committed figures does develop it, and it carries **166.3 of the 311.5** uplift,
   while 2025-26 Q2, which the block does name, carries **0.0** (its age-5 factor is 1.000). As written the block
   names the one developed quarter that moves nothing and omits the one that moves most of the answer.
   Per-quarter uplift: 2025-26 Q2 +0.0, Q3 +11.7, Q4 +43.2, 2026-27 Q1 +90.3, 2026-27 Q2 +166.3.
2. **"Cycle IP-11" is ungrounded.** No shipped file contains "IP-11". `improvement_placements.csv` ends at IP-10
   (2026-27 Q3, unit 41460, in progress) and `placement_cycle_notes.txt` heads itself "Notes on the IP-10 placement
   cycle (quarter from 1 April 2027)" while its own body says the team "finishes at Rehabilitation and Aged Care on
   31 March and starts wherever we land on 1 April". The input file is internally loose; since nothing graded turns
   on the label, repair the write-up (drop the cycle identifier) rather than the file, which would void prior runs.
3. **Inverted sentence, Final Recommendation.** 41220 "falls to 27.8" - developing raises it from 26.1 to 27.8;
   it falls in rank, not in value. Restate.
4. **Inverted sentence, Critical Component 2.** "A quarter of cost centre 41210's coding carries 1.763 of its
   eventual count at its own close" - at its close a quarter carries 1/1.763, i.e. about 57 percent, of its eventual
   count; 1.763 is the multiplier from close to ultimate. Restate.
5. **Step 7's lower bound does not reproduce.** "between 1.528 and 1.608 times": across eight development variants
   I measured 1.530 to 1.608. Substance holds (all variants name 41210); the stated bound should read 1.530.

## Files / Hygiene: PASS

21 files; 4 formats (15 csv, 2 pdf, 1 xlsx, 1 txt). `episode_outcomes_extract.csv` is 465,881 data rows / 34 MB.
No README, no synthetic or benchmark disclosure, no tool banner, no solver-facing language; `quality_dashboard_2026q2.xlsx`
carries in-fiction metadata only (creator Joseph Hunter, created 2027-03-05) and has no hidden third sheet. Dates
cohere: export 2027-03-05, coding close 28 February, committee 24 March 2027, assessment quarter from 1 April 2027.
Realistic mess is genuine and unplanted: 1,546 duplicate episode rows against the dictionary's own separation key;
blank `comorbidity_score` on about one episode in seven, worse in January and winter; 960Z/961Z error DRGs;
two revisions of the national list with HAC03-HAC06 renumbered and HAC13 folded in at 2026-07-01; 41520 reporting
under Carrowdean to June 2026 then Marrowfield, so the site a unit reports under changes mid-series; 41511/41512
amalgamated into 41510 on 2025-09-30; the detail extract missing the Carrowdean campus; fiscal against calendar
years in the asks; the activity summary and the extract disagreeing for 41250 (April-May 2026) and 41350
(July-August 2026) exactly where uncoded episodes sit. No file reads as machine-authored. No public-data
contamination (invented network, no canonical published finding). Nothing exclusion-level.
One low-severity coherence note: `placement_cycle_notes.txt`'s header labels the April-2027 cycle IP-10, which the
placement register assigns to 2026-27 Q3. Non-decisional.

House Gate G (no shipped artifact ranks the candidates and gets it wrong): satisfied. `quality_dashboard_2026q2.xlsx`
is sorted alphabetically, ranks nothing, covers one closed quarter, is stamped "Quarter-end position; not a
projection of any later quarter", and is arithmetically correct for what it is (41210 Q2 218 complications matches
the register's first publication of that quarter exactly). It is nonetheless the sharpest honest trap in the pack,
because at SR 0.738 it makes the recommended unit look like the best in the network.

## Stump power (Gate F)

Strong. Both easy routes are available and both are wrong: ranking on `unit_indicator_series.csv` as reported gives
Alderbrook General Surgery 41220 at 26.1, and reading the dashboard's latest quarter makes 41210 (SR 0.738) look
like the strongest unit in the network. Reaching 44.6 needs four correct moves - seeing that the close-out register
is a development triangle rather than a restatement log, reading charter 4.3's "the complications its own patients
had" as ultimate rather than coded-to-date, estimating age-to-ultimate factors per unit instead of pooled (the
pooled factor gives 41220), and applying spec 3.4's per-separation basis to the planned quarter. No too-easy signal
is present: no file documents the lag as a defect to correct, the word "develop" appears nowhere in the pack, and
the deciding quantity is a computation, not a rule to find.

## Stumping type (Gate G)

`mechanism: forecasting`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`,
`sole_data_defect: no`.
Every reported number is fine and stays fine: the close-out register publishes each quarter honestly as at its
publication date, the indicator series equals the register's latest publication for every unit, the dashboard is
correct for the one quarter it covers, and the denominators are not censored at all. The decision turns on a forward
quantity - avoidable complications on a quarter of planned separations that has not begun - which the correctly-read
past does not pin because the complication counts are right-censored by coding lag, exactly the "lead-time or
censoring effect the history shows" shape. The history supplies the development pattern, and `cis_registered_date`
supplies its mechanism. Nothing has to be caught as wrong, so this is not surface-read-rejection at any depth;
`banned_stumping_type` does not apply. Clean-data test: on fully coded data the triangle would still be the object
and the forward projection would still have to be made, so the task does not collapse.

## Three rules (Gate H)

`domain: pass`, `layers: pass`, `decisive_step: analytical`.
H1: the deciding quantity is a risk-adjusted excess-complication count - observed against expected from published
risk-band-by-age strata, carried to ultimate for coding lag and projected onto planned activity - which is the core
work of a health-service clinical indicator analyst, not a setting. Swap test run: substituting energy or education
nouns breaks the task, because the risk-adjustment strata, the acute-multi-day denominator, the national
complication list revisions and the coding close-out cycle are health-data constructs with no analogue.
H2: Layer 1 is the network's own mess (duplicate episode rows against the stated separation key, two list revisions
renumbering HAC03-HAC06, a unit that changes reporting site mid-series, amalgamated cost centres, a campus missing
from the detail extract, fiscal against calendar years, uncoded episodes making the summary and the extract
disagree). Layer 2 is the rigour that decides it: recognising right-censored quarterly counts and developing them
to ultimate on a unit-specific pattern the data itself justifies.
H3: analytical. The easy route a strong analyst who cleaned every file and read every rule correctly still takes is
to rank the 12 eligible units on observed minus expected as the series reports it, which files **Alderbrook General
Surgery, cost centre 41220, at 26.1** - or, worse, to read the quarter dashboard and conclude 41210 is the network's
best unit. Neither is a defect to catch, a decoy, a field to read or a rule to execute; both are the analysis done
the easy way.

## Fix

**solution.** Regenerate Critical Component 1 and Solution Step 3 to say five of the ten closed quarters have not
settled, naming 2026-27 Q2 and its 166.3 of the 311.5 uplift; drop "cycle IP-11" from the Final Recommendation;
restate 41220 as rising to 27.8 rather than falling; restate Critical Component 2's factor the right way round; and
correct Step 7's lower bound to 1.530. No input file is touched, no graded figure moves, no rerun is required.
