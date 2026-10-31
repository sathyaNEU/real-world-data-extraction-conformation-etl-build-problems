# determinism-check report, task195, 2026-10-31 (pass 2, reship under the 10-30 gates)

## Verdict
NOT_DETERMINISTIC on the asks (Q3, Q4); DETERMINISTIC on the main call (0.030), with one exposure noted below.
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method/model selection, stumping_family: paired-estimand choice, surface_read_dependency: no, sole_data_defect: no

## Why
The isolated thread (verdict at /tmp/determinism-check-task195-pass2/verdict.md) reproduced the main call: 5,839 specimens (393 events, 5,446 clean), 292 / 91 for the screen in service, candidate detections 294/308/310/319/326, false calls 61/74/80/85/104, increases 0.51/4.07/4.58/6.87/8.65 points, 0.030 the highest cutoff meeting 4.1(a) and (b). Two asks rest on readings filed nowhere:
- Q3: "distinct vials" is defined in no shipped file (the export manifest and dictionary that once carried it were removed). The golden equals distinct biobank_ref via the crosswalk. Distinct specimen_id gives 585, specimen plus aliquot 587, plate_barcode 583 for W13 (golden 575).
- Q4: the golden needs the release amendment log applied and a distinct-specimen denominator; the prompt states neither. Unamended data gives 18.4 ...; the volumes file's results count as denominator gives 16.2 ... or 12.4 ... Neither matches (underspecified_objective).
Q5 reproduced and robust (counts do not move under the label-level reading).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Population / events / clean | 5,839 / 393 / 5,446 | same | yes |
| In-service detections / false calls | 292 / 91 (1.67) | same | yes |
| Candidate detections (0.050 to 0.010) | 294/308/310/319/326 | same | yes |
| Candidate false calls | 61/74/80/85/104 | same | yes |
| Increase, points | 0.51/4.07/4.58/6.87/8.65 | same | yes |
| Paired interval 0.050 / 0.030 | fails / clears | b=14,c=12 fails; b=23,c=7 lower bound +1.37 | yes |
| Q3 W13 to W21 | 575,14 ... 538,26 | yes, only as distinct biobank_ref | yes, one reading only |
| Q4 twelve months | 15.6 ... 16.1 | yes, only with amendments applied, RELEASED rows, distinct-specimen denominator | yes, one reading only |
| Q5 L1/L2/L3 | 0.963,7 / 0.865,7 / 1.027,6 | same | yes |

## Competing answers that survived
1. Q3: vial identity (biobank_ref 575 / specimen_id 585 / specimen+aliquot 587 / plate_barcode 583). No shipped rule closes it. Open.
2. Q4: raw versus amended history, and distinct-specimen versus results-count denominator. No shipped rule closes it. Open.
3. Main call (exposure, not a failed fork): KVAL-07 4.1(a) names no interval estimator. Independent proportions on 292/393 against 308/393 give a 0.030 lower bound of -1.9 points and recommend 0.015. The thread holds the paired reading is forced by the design (same 393 specimens), but a grader could call it unfiled.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats | 10+ / 3+ | 17 / csv, tsv, xlsx, json, pdf | yes |
| Large file | 25,000+ rows | qc_screen_history 32,647 rows | yes |
| Distractors | 2+ in metadata.json, none named by file name | 4 declared (assay_unit_costs, extraction_platform_validation, lims_run_log, plate_layout_map), none labelled by name | yes |
| Distractors unused yet weighable, ruled out by a shipped fact | yes | thread cross-checked lims_run_log and layout map for window/project agreement only; none answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | yes (closing sentence of the prompt) | yes |
| Prompt shape, rubric 25+ criteria | yes | prompt 996 chars, one paragraph; rubric not generated here, count not verifiable by me | not verified |
| No LLM tell, goldens business-real | yes | not assessed by the thread; leave to golden-realism | not verified |
| No describing file shipped | yes | manifest and dictionary absent from the 17 files | yes |

## Gate G reconciliation
Thread: mechanism method/model selection, family paired-estimand choice, surface_read_dependency no, sole_data_defect no. Gate H: domain pass, layers pass, decisive_step analytical. Design note and metadata.json (read after the thread): the note declares the same decisive step (interval from the discordant specimens) and the same Layer 1 / Layer 2 split, so the thread and the design agree on mechanism, family and Gate H. The declared distractors are not named by the thread as carrying the task, so none is too load-bearing. No mismatch on the Gate G fields.

## Stump power (Gate F)
The thread rates it strong: the easy route (each screen with its own interval, or an unpaired test) holds the change or lands 0.015. Weigh this against the design note's own earlier measurement, recorded in its history: 6 of 12 enumerated routes (paired Wald, McNemar, exact McNemar, bootstrap over specimen rows, permutation, clustered regression) file 0.030 once the population rebuild yields one row per specimen, the analyst test was recorded as failing, and a scored reader had landed the call. The golden is the textbook paired method for two classifiers on shared units (stumping 1.3), so the call is landable by a strong solver. The thread's "analytical" classing and the design note's own record are in tension; the main thread should weigh it against the ladder. The asks (Q3 key reconstruction, Q4 amendments with date moves) are hard but are currently the open forks.

## Findings, ranked
1. Q3 vial identity unfiled (underspecified_objective); the removed describing files used to carry it.
2. Q4 basis unfiled: amendment log application and distinct-specimen denominator.
3. Main call estimator not named in 4.1(a); the competing unpaired answer lands 0.015. Do not close it by filing the HOW (determinism-check section 1).
4. Stump power: landable by the standard paired method per the design note's own measurement.
5. Rubric criteria count and golden realism not verified here.

## Next action for the author
Fix the generator so the identities are filed in prompt wording or a non-describing shipped rule, not a describing file: name the vial identity by its biobank reference in Q3 and state that the release amendment log applies and that released specimens are counted distinct in Q4. No golden figure moves. Then rebuild twice, re-run the gates and re-judge once. Closing findings 3 and 4 is a separate decision for the main thread.
