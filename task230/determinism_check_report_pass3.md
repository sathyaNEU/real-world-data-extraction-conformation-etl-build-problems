# determinism-check report, task230, 2026-11-01 (pass 3, the 11-01 re-check)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Run
One isolated thread (general-purpose, Sonnet, medium) on a fresh unzip of the re-check cut at
/tmp/determinism-check-task230-r5/target/, briefed with guidelines/determinism_judge_system_prompt.md verbatim, the
prompt and the submission's graded blocks. The determinism-judge agent type was not loadable after a container
restart, so the main session held the wrapper's role under .claude/agents/determinism-judge.md (the thread isolated,
the spec gates and the Gate G and H reconciliation done after it returned). The thread judged the cut before the
trim that answered the leak reader's realism tell (procedures 4 and manual 5.6, below); no graded figure moved.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | csv, docx, parquet, pdf, xlsx | yes |
| Large file | 25,000 rows | census2026_receipt_register.csv, 541,954 rows | yes |
| Distractors | 2 or more, named in metadata.json, none in a file name | LFS 2026 Q3 and the 2021 census counts | yes |
| Deliverables | 1 to 3, each in the golden | occupation_coding_warnings_2026.xlsx, occupation_coding_bias_2026.png | yes |
| Asks | multi-dimensional, unit and rounding stated | teams by write-ins and hours, regions by calls and no-contact calls; hours to two decimals | yes |
| Rubric | 25 or more criteria | 40 groups' biases, the call, 10 team and 16 region figures | yes |

## Gate G reconciliation
The thread's forecasting / analytical_non_defect / no surface read / no sole defect matches the card (Gate G
forecasting, stump_class analytical) and the design note's decisive step (the study's bias carried by response route
to the write-ins still to code under the 0.80 score). It named neither distractor as the surface read.

## Gate H
domain pass, layers pass, decisive_step analytical. The leak reader's question 6 on the same cut read the call as
following stated rules plus catching the wider release population; the judge recomputed the rule-only route
(OQ-4 2.1, 3.1 to 3.3 and the 0.80 Decision executed on the coded-so-far mix: 35, 41 and 93) and the pooled
follow-up carry (24, 35, 41 and 93), both wrong, so the judge settles it (build-pipeline, stage 4).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Coded by route | 321,660 / 122,864 / 71,258 / 15,330 | identical | yes |
| Still to code by route | 3,344 / 1,925 / 44,986 / 53,112 | identical | yes |
| Release population | 634,479 | 634,479 | yes |
| Six warned groups | -3.1, -2.5, +4.6, +3.2, -2.3, +6.9 | -3.08, -2.51, +4.63, +3.20, -2.27, +6.88 | yes |
| The other 34 groups | within plus or minus 2.0, one decimal | all match | yes |
| Team October write-ins | 4,160 / 3,746 / 4,206 / 3,112 / 2,680 | identical | yes |
| Team October hours | 295.75 / 270.75 / 283.00 / 229.50 / 176.00 | identical | yes |
| Region September calls | 20,016 / 10,468 / 9,289 / 10,084 / 8,380 / 8,867 / 8,438 / 7,435 | identical | yes |
| Region no-contact calls | 8,208 / 4,215 / 3,798 / 4,163 / 3,367 / 3,611 / 3,471 / 3,055 | identical | yes |

## Competing answers that survived
None. Forks tested and closed: team placement by the day coded or the shift's day (same), the register's static
team (ruled out by the movements file and procedures 4), hours by the line's entry date (ruled out by procedures 4,
"A timesheet line is dated by the day its shift began", kept in the final cut for this reason), re-sent calls (the
data and manual 5.6), sync time against call time (manual 5.2 records each call on the tablet at the doorstep; the
log's own visit_time and synced_at), score drift across load months (none).

## Stump power (Gate F)
Substantial on paper: the coded-so-far bias, the pooled follow-up carry and the routes under 0.90 each file a
specific wrong set; the route is no column and needs the visit log. Caveat: a bootstrap of the study puts about 0.3
points of standard deviation on groups 25 and 71; OQ-4 4.1 tests the unrounded point estimate, so the call is forced.

## Findings, ranked
1. Minor, non-decisive: one timesheet correction for 27/10 entered on 2 November in an export named to 1 November;
   the export is by shift date and the line is dated by its shift, so harmless.

## Next action for the author
None for determinism.

## Thread's verdict (verbatim)

# Verdict: task230 (re-check 2026-11-01)

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. Every committed figure reproduced from the shipped files, so no repair is needed and no rerun is required. One optional lever is listed under Fix.

**Why:** The six warned groups (24, 25, 35, 41, 71, 93) fall out of one chain that the files pin step by step. The chain is: OQ-4 2.1 (uncoded write-ins belong to the release population), OQ-4 3.1 to 3.3 (the bias formula, and estimates from the study weighted by selection interval), the processing plan Decision sheet (0.80 score from 16 Nov), and field manual 5.3 and 5.5 (route from the call outcome). The closest unwarned groups sit about 1 pt inside the lines (26 at -1.07, 43 at +1.04). The closest warned groups sit 0.27 and 0.51 pt outside them (71 at -2.27, 25 at -2.51). Those gaps are cleanly calculable. The estimator is unambiguous, because weighting by interval and scaling to the extract counts give identical results. The three supplementary tables (bias for all 40 groups, team write-ins and hours, region calls and no-contact calls) are fixed by the procedures PDF, the staff movements file and the field manual. I found no surviving alternative answer under a reasonable reading.

## Evidence (recomputation ledger)

| Figure | Claimed | Recomputed | Reproduced |
|---|---|---|---|
| Coded by route (online / paper / household member / proxy), census2026_occupation_coding_extract.parquet joined to receipt_register and field_visit_log (outcome 10 or 20 by questionnaire_id) | 321,660 / 122,864 / 71,258 / 15,330 | identical | Yes |
| Still to code by route | 3,344 / 1,925 / 44,986 / 53,112 | identical (register occupation_writeins minus coded) | Yes |
| Release population | 634,479 (531,112 coded, 103,367 to code) | 634,479; the processing plan "Position 13 Nov" sheet agrees | Yes |
| Six warned groups and biases (route-stratified, 0.80 score, interval-weighted study) | 24 -3.1, 25 -2.5, 35 +4.6, 41 +3.2, 71 -2.3, 93 +6.9 | -3.08, -2.51, +4.63, +3.20, -2.27, +6.88 | Yes |
| The other 34 groups (all within +/-2.0) | listed in the supplementary answer | all 34 match to one decimal, and all are inside the lines | Yes |
| Wrong-method decoys | coded-so-far warns 35 and 93 only | 35 (+2.27) and 93 (+3.15) | Yes |
| | pooled follow-up warns 24, 35, 41, 93 | 24 -2.22, 35 +3.06, 41 +3.43, 93 +4.85 | Yes |
| | routes under 0.90 warn 24, 35, 71, 93 | 24 -2.42, 35 +3.29, 71 -2.27, 93 +6.40 | Yes |
| Team October write-ins, with team placed by coder_id and day from coding_staff_movements (CLERICAL path, coded_at date) | T1 4,160; T2 3,746; T3 4,206; T4 3,112; T5 2,680 | identical (17,904 in total, with no unplaced coder-days) | Yes |
| Team October OCC hours (work_date in October, staff_no placed by day, negative lines included) | 295.75 / 270.75 / 283.00 / 229.50 / 176.00 | identical | Yes |
| Region September calls and no-contact calls (outcome 31) after removing re-sent duplicates (same address, call time and outcome, later sync) | 20,016 / 10,468 / 9,289 / 10,084 / 8,380 / 8,867 / 8,438 / 7,435 | identical for all 8 regions | Yes |
| | no-contact: 8,208 / 4,215 / 3,798 / 4,163 / 3,367 / 3,611 / 3,471 / 3,055 | identical for all 8 regions | Yes |

**Source fields.**
- Route: receipt_register `capture_mode`, plus field_visit_log `questionnaire_id` and `outcome_code` for FIELD forms.
- Study: `selection_interval`, `autocoder_code`, `autocoder_score`, `production_code`, `reference_code`.
- Teams: extract `coder_id` and `coded_at`; staff movements.
- Hours: timesheets `staff_no`, `work_date`, `activity`, `hours`.
- Regions: field_visit_log `ed_code` mapped through enumeration_districts.

**Route detail.**
- 391 outcome-10/20 questionnaire_ids appear twice in the visit log. These are tablet re-sends with the same outcome.
- 162 addresses have a proxy interview followed by a household-member interview. The withdrawn proxy questionnaire is absent from the register, so the route is unambiguous.
- All study doc_ids map to a route.
- Study weights per route (71,298 / 321,678 / 122,786 / 15,300) track the coded counts closely, which confirms the route mapping.

**Forks tested.**
- Team placed by `coded_at` date versus by shift date: identical result.
- Team taken statically from the register: wrong (3,916 / 3,887 / 3,768 / 3,471 / 2,862). The movements file and procedures section 4 forbid it.
- Hours by `entered_on` instead of `work_date`: 312.00 / 273.00 / 292.00 / 246.50 / 181.25. Procedures section 4 dates a line by the shift start, and the correction lines' `work_date` carries the shift they correct, so this reading is not licensed.
- Region calls without removing re-sends: overcounts by 759 calls in total (e.g. 10,552 against 10,468 for Ardvale). A call cannot be made twice at the same minute at the same address with the same outcome, and field manual 5.6 documents replacement tablets, so the removal is forced by the data's own logic.
- Counting by `synced_at` instead of `visit_time`: the manual says the tablet stamps the call time, so `visit_time` is the call time.
- Score drift in the study across load months: none. Share under 0.80 is stable at about 0.09 for household members and 0.10 for proxy, and the 21.9% / 8.95% in the plan's Capacity sheet agree. Applying the study's route rates to the later batches is therefore supported by the data.

**Residual caveat (not a determinism failure).** Bootstrap of the study gives a standard deviation of about 0.3 pt on the biases of 25 and 71. The standard (OQ-4 4.1) tests the unrounded point estimate and asks for no significance test, so the call is forced. A reviewer should know the margins for 25 and 71 are within roughly 1 to 1.5 standard errors of the line.

## Gate B location check
- 0.80 acceptance score: processing plan, Decision sheet (2026-11-12).
- Unpinned elements in the prompt (13 Nov position, route stratification) derive from the files: the Position and Decision sheets, plus manual 5.3 and 5.5.
- 2.0 per cent line: OQ-4 4.1.
- Reference code definition: OQ-4 3.2.

## Files/Hygiene
- **PASS.** 15 files in 5 formats: csv (10), pdf (2), parquet (1), xlsx (1), docx (1). The files read as operational artifacts, with a change-log style movements file, correction lines and sync stamps. I found no README or authoring disclosures.
- Minor note: the timesheet line S41303 for 27/10 was entered on 2 Nov, after the file's stated 01Nov end. The line is dated by shift, so this is harmless and not decisive.
- The census2021 and LFS files are context. I found no sign that they drive the golden.
- No public-data contamination: the data is a fictional country (Aldmere).
- The PNG is not independently verifiable beyond its spec (40 bars, lines at +/-2.0).

## Stump power (Gate F)
Substantial. The naive routes each give a specific wrong list:
- Study coded-so-far bias warns only 35 and 93.
- Follow-up carried as one batch type warns 24, 35, 41 and 93, and misses 25 and 71.
- Routes carried under 0.90 warns 24, 35, 71, 93 and misses 25 and 41.
- Pooling everything warns 35, 41, 93.

The mix shift is strong: follow-up coded so far is 82% household member, but the follow-up still to code is 54% proxy. Proxy bias is 3 to 5 times larger. The route is not a study column and needs a visit-log join. The prompt gives no hint of route stratification. I recommend live runs to confirm that GPT runs fail on this, because there are no model responses to adjudicate.

## Stumping type (Gate G)
`mechanism: forecasting` (population projection with a mix shift, plus a rule change from the 0.80 score), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
The study figures are correct. The difficulty is carrying them forward to the release population by route stratification and the 0.80 rule. On perfectly clean data this would still stump a model that pools.

## Three rules (Gate H)
`domain: pass`, `layers: pass`, `decisive_step: analytical`
- Layer 1 (messy data): route lives in a different file, tablet re-sends, a withdrawn proxy questionnaire, reused coder ids, correction lines, and a statistical study with unequal intervals.
- Layer 2 (rigour): post-stratified estimation of coding bias from a quality study, projected to a mix-shifted uncoded population.
- This is census quality-measurement work, so the swap test fails and the domain is genuinely used.
- Easy route: apply the study's coded-so-far or pooled follow-up rates. That gives 2 to 4 groups and wrong lists.
- The teams and regions tables are rule application, but they are supplementary only.

## Cross-batch check
I found no match against prior packages. I was not given a prior-package archive in the isolated directory, so this check is limited to what was visible.

## Fix
None required (fix location: none). Optional: nothing needs changing in the solution blocks. The solution steps and critical components match the files.
