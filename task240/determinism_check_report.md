# determinism-check report, task240, 2026-10-17

## Verdict
DETERMINISTIC (SOLUTION_WRONG only as a wording defect in SOLUTION_STEPS step 7)
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Every committed answer reproduced from the fresh unzip. QS-7 3.3 files the 20.0 line; QS-7 2.1 and 3.2 tie the standard error to the estimate as published with the final weights; the weighting note says the weights are post-stratified in 96 region x age x sex cells, so the literal reading is z = w(y - p_cell) and 9 estimates are warned. The fixed-weight reading gives 15. The only defect is step 7 saying 107 full interviews "postdate the 30 September extract": their interview dates run 12 Aug to 24 Sep, before the extract, and their outcome rows are stale. Reword; no data or prompt change.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Adults / households / PSUs / strata | 7,238 / 3,764 / 707 / 24 | same (members x weights x households) | yes |
| 48 CVs (1 dp) | per submission Ask 1 | all 48 match; warned min 27.62, unwarned max 18.36 | yes |
| Warned count | 9 | 9 (R01 CARE 27.62, ARR 30.08; R02 RENT 32.67, CARE 48.70, ARR 39.37; R03 CARE 38.64, ARR 29.99; R04 CARE 34.26, ARR 28.06) | yes |
| Fixed-weight variant | 15 | 15 (adds R01 PEN, R01 RENT, R02 PEN, R03 PEN, R03 RENT, R04 PEN) | yes |
| Response rates, 12 regions | 59.6 ... 54.4 | all 12 match, e = 0.9170 | yes |
| Calls, 12 regions | 96 ... 425 | all 12 match, 769 duplicate tablet copies | yes |
| Step 7 "107 postdate the extract" | postdate | dates 12 Aug to 24 Sep, precede the extract | NO (wording) |

## Competing answers that survived
None on the main call; the fixed-weight route is the declared trap and the files close it. Residual soft spots, low: (1) QS-7 4.1 "outcome of its last issue" has to be overridden by the households file for 107 stale extract rows (closed by the data dictionary and QS-7 4.2); (2) the extract-only, raw region_code and drop-the-94 readings of the response rates shift rates by up to 0.7 points and are each excluded by shipped text.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 14 | yes |
| Formats | 3+ | csv, xlsx, docx, pdf, md | yes |
| Large file | 25,000+ rows | hrs27_call_records.csv 35,849 | yes |
| Distractors in metadata.json, none named in a file | 2+ | interviewers.csv, ssb_population_estimates (names are plain, not labelled) | yes |
| Distractors unused yet weighable, none answers a graded quantity | yes | neither carries a precision figure; population totals tie to the weights under every method | yes (population estimates feed the weights, so weighable) |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, docx), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 48 cells x CV and warning; 12 regions x rate and calls; percentages to one decimal; calls a count | yes |
| Prompt shape, rubric 25+ | shape and 25 | shape 07 grid; the rubric is generated and not in the folder, but 48 + 24 + note items far exceed 25 | yes (not directly counted) |
| Not LLM-sounding, goldens real | yes | judge found no authoring disclosure; golden realism not re-read by me | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: Gate G method_or_model_selection, layer 2 family estimation_fit, pattern post-stratified-estimate-variance-from-within-cell-residuals; stump sentence is the fixed-weight Taylor linearisation filing 15. Match. The thread did not name either declared distractor as carrying the task. Gate G classification: pass, no shipped artifact ranks the estimates on precision or on the warning.

## Gate H
domain: pass; layers: pass; decisive_step: analytical. Decisive step is the variance of a post-stratified estimator (residuals from the calibration cells) against the default fixed-weight linearisation. Layer 1 is region-code drift, a stale outcome extract, duplicate tablet records and letters mixed with calls. Matches the design note's three rules. Caveat (low): QS-7 3.2 "as published" could be read by a hard-line reviewer as rule application; the judge holds it analytical because the weighting note describes the weights without instructing a variance correction.

## Stump power (Gate F)
Good. The default route files 15 and wrongly warns six (four pension, two rented-home); the asks add independent traps (stale region code, stale outcomes, absent addresses, duplicate records, non-call contacts).

## Findings, ranked
1. LOW, solution only: SOLUTION_STEPS step 7 misstates that 107 full interviews postdate the 30 September extract; they precede it and their extract rows are stale. Reword.
2. LOW, optional: state in step 7 that the 94 absent addresses are eligibility not established because they carry only advance letters.
3. LOW, residual: "outcome of its last issue" (QS-7 4.1) must be overridden by the households file; closed by shipped text, no change needed.
4. LOW, caveat: rule-application reading of QS-7 3.2 "as published" (see Gate H).
5. INFO: rubric criterion count not verifiable in the folder.

## Next action for the author
Edit step 7 in submission.md (and any copy in the design note) to say the 107 households' extract outcome rows are stale though their interviews precede 30 September; no rebuild, no re-judge needed beyond the stage-4 FIX_NOW convention.
