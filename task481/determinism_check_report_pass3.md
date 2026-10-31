# determinism-check report, task481, 2026-10-31 (pass 3; the brief directory is /tmp/determinism-check-task481-pass2/)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated thread (sonnet, medium) read only the fresh unzip. It reproduced every committed answer with the prompt and filed definitions executed literally: 5,254 for 2025, 5,193 (about 5,200) for 2024 restated, +1 per cent, and all 24 quarterly shooting figures. The main call is forced by the stratified conversion of line 4e (domestic victims 21.2 per cent coded 13A, others 0.31 per cent; domestic share 35.8 per cent in Oct-Dec against 29.1 per cent in Jan-Sep). The easy route, Q4 rates applied uniformly, gives about 5,400 and -3 per cent. The pooled letter ratio (1,204/1,076) lands in the same place. The state's 10.2 per cent reproduces (5,320/4,829) and is ruled out by its date-of-incident basis. Removing the data dictionary and field notes did not open a fork: the code list, General Order 417 and the methods sources section carry the definitions.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| 2025 13A, month reported, local time | 5,254 | 5,254 (UTC-year reading gives 5,264; methods fix local time) | yes |
| 2024 published, Return A 4a-4d col 4 | 4,829 | 4,829 | yes |
| Q4 2024 13A | 1,204 | 1,204 (matches certification letter) | yes |
| Q4 share 13A: 4a-4c, 4d | 100%, 32.4% | 100%, 135/417 = 32.4% | yes |
| Q4 share 13A: 4e domestic, other | 21.2%, 0.31% | 348/1,642, 9/2,948 | yes |
| Domestic share 4e, Oct-Dec / Jan-Sep | 35.8% / 29.1% (4,756 of 16,321) | same; Q4 DVU months 491/535/616 match the extract | yes |
| Hierarchy-unscored victims | 202 | 53 in Q4 plus 148.9 scaled, about 202 | yes |
| Restated 2024 | 5,193, about 5,200 | 5,193 | yes |
| Change | +1% | +1.17% on 5,193, +1.04% on 5,200 | yes |
| Shooting grid, 12 quarters, victims and shootings | 110/105 ... 126/115 | all 24 match | yes |

## Competing answers that survived
- The restatement: the pooled or per-line Q4 conversion (5,400, -3%) is a cruder estimator of the same estimand and the data separate it (the 4e rate rises with domestic share month by month). Not a semantic fork. The reasonable variants all land on 5,200 and +1%: stratifying 4d about 5,196, counting unfounded DVU cases about 5,235, dropping the homicide NS term 5,173. Omitting NS entirely (5,044) is wrong, because the letter and code EPD-2 say NIBRS counts the hierarchy-hidden victims.
- One residual, on supplementary ask 2 only: the shooting log's time zone is unlabelled. The UTC reading of records entered from 1 October 2024 is inferable from the files, but the thread notes the text does not state it for the log. The evidence is the extract note, 22 re-entered rows shifted +5 or +6 hours, and the hour-of-day profile. Not converting gives wrong figures (2024 Q3 189/172 against 169/153). Optional one-line pin in the methods note, not required.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files, formats, large file | 10+, 3+, 25,000+ rows | 16 files; csv, xlsx, pdf, docx; extract 119,713 rows | yes |
| Distractors | 2+ in metadata.json, none in a file name | 3: census estimates, CAD calls, state repository download; no file name labels one | yes |
| Distractors unused, weighable, ruled out | yes | state table 8 and download give 5,320 / 10.2% (reproduces), ruled out by the date-of-incident basis; census and CAD unused | yes |
| Deliverables | 1 to 3, all in golden | 1 (xlsx), present in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 12 quarters by two counts plus restated total, 2025 and change; rounding in the prompt | yes |
| Prompt shape and 25+ criteria | shape identifiable, 25+ | shape 07 (grid of cells); 24 grid cells plus 3 headline figures plus components exceed 25 (rubric is generated, count not independently checkable here) | yes |
| Reads as real, not LLM generated | yes | thread found system-artifact files, coherent dates, no disclosure | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: Layer 2 estimation_fit, decisive step the stratified conversion of line 4e, easy route the per-line conversion at about 5,400 and -3 per cent. These match; the thread names the same easy route (uniform or pooled Q4 rates, 5,400, -3%). The declared distractor (state 10.2%) is not the surface read carrying the task, so it is not too load-bearing. No shipped artifact ranks the call wrongly: the certification letter reports its own Q4 comparison and recommends no restatement. Watch: the letter's 1,204/1,076 ratio hands a solver the easy route's input. It is an honest official figure, not a ranking.

## Gate H reconciliation
Thread: domain pass, layers pass, decisive_step analytical. Design note: domain test (back-casting a series across a coding break), Layer 1 (layout changes, UTC against local, renumbered ids, state basis), Layer 2 (conversion level and composition), decisive step analytical, with the analyst test executed in checks.py on clean truth (-2.1 against +2.1). They match. The thread did not class the step analytical merely because the method is textbook: it found the standard per-line route files the wrong answer.

## Stump power (Gate F)
High on the main call: a strong analyst who cleaned the data and read every rule would file 5,400 and -3 unless they stratify line 4e by domestic status, and the state's 10.2% pulls the other way. The asks are hard (outside-block rule by block, UTC re-entries, ME matching on block, age and sex, shooting as a block-minute pair). The main thread weighs this against the design note's ladder.

## Findings, ranked
1. Residual, low: the shooting log's UTC convention for records entered from 1 October 2024 is inferred from the files, not stated. Supplementary ask 2 only; the main call is unaffected.
2. Watch, low: the letter's pooled 1,204/1,076 ratio sits beside the easy route. It is honest and rules nothing out.
3. No fork on the main call; the reduced pack (no dictionary, no field notes) remains closed.

## Next action for the author
Ship. Optionally add one sentence to the methods sources section that records entered from 1 October 2024 in the shooting log carry UTC times, which needs no rerun of the analytic surface.
