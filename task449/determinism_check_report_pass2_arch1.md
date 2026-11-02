# determinism-check report, task449, pass 2, 2026-10-12

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Re-judge after the pass-1 FIX_NOW (Marlowby export ids and dates). One isolated thread (general-purpose, sonnet, medium) on a fresh unzip at /tmp/determinism-check-task449-r2/target/. Every committed answer reproduces and is forced by the prompt, WPS-3 (2.2, 3.1, 4.1, 4.2) and Schedule 7 (7.1, 7.2). The share of name-and-city matters arising from the failure is estimated (k=1 subset 478/597 = 80.07%, all-k inversion f = 0.7989 against the 4.0% portfolio rate), and every estimator lands on 500, 950, 35. 35 holds for an incident total of about 3,897 to 4,117; the estimators span 3,994 to 3,999, so the margin is about 100 matters and uncontested.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| New matters in window, merged out | 11,597 | 11,609 less 12 = 11,597 (1,449.6/wk) | yes |
| Verified four-code, on Meridel list | 2,081 | 2,081 | yes |
| NAME_CITY four-code | 2,395 | 2,395 (851 attach affected) | yes |
| k=1 | 478 of 597, 80% | 80.07% | yes |
| Failure matters a week | 500 | 499.3 to 499.9 | yes |
| Sustained base | 950 | 949.8 to 950.4 | yes |
| Analysts | 35 | 34.5 to 34.56, up | yes |
| Month-end open | 720,730,710,740,8260,5590,3230,2230,1850 | 721,728,710,739,8260,5589,3232,2232,1849 | yes |
| Flex hours | 790,670,760,720,3430,4120,3440,2830,2170 | 791.5,671.75,761.25,721.5,3431.75,4121.25,3441.5,2831.75,2171.25 | yes |

## Competing answers that survived
None. Attached account at face value gives 40; verified-only gives 44 (7.2 covers by the cardholder's account, not by confirmation); October weeks excluded by 3.1; merged duplicates excluded by 2.2; returned-unpaid accounts hold no window matters. The 44 reading is closed by SF1(c) in the design note.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 17 | yes |
| Formats | 3+ | 4 (csv, pdf, xlsx, jsonl) | yes |
| Large file | 25,000+ rows | 77,145; 159,488; 67,969 | yes |
| Distractors | 2+ in metadata.json, none in a file name | IVR weekly, CFPB public file; names do not label them | yes |
| Distractor weighs, unused, ruled out | yes | relevant to complaint volume, unused, no contamination; not shown to reproduce a graded quantity | yes, light |
| Deliverables | 1 to 3, all in golden | 2 (docx, csv) | yes |
| Asks unit and rounding | yes | nine-month series and counts; rounding stated once in the prompt | yes |
| Prompt 720 characters, shape identifiable | yes | shape "other" in metadata | yes |
| Rubric 25+ criteria | yes | not generated or checked in this pass | not verified |
| Reads as real | yes | judge: system-like mess, no authoring leakage | yes |
| Hygiene (dates vs 9 Oct pull) | no file postdates | Marlowby final export now MSX-20261003 (dated 2026-10-03 per manifest), last export 1 Oct; coherent | yes (pass-1 finding closed) |

## Gate G reconciliation
Judge: statistical_rigor / analytical_non_defect / surface_read no / sole_data_defect no. Card and design note: stump_class analytical, generators G17 then G3, gate_g method_or_model_selection, no decoy, no decisive rule filed. Match. Declared distractors are not the surface read carrying the task. Easy routes (40, 44) equal the note's default path and imputation path.
Gate G line: PASS.

## Gate H line
domain: pass; layers: pass; decisive_step: analytical (estimating the true incident share behind first-of-k name-and-city attachments). Matches the note's Three rules.

## Stump power (Gate F)
Plausible and unmeasured. A strong solver who reads everything still files 40 or 44 unless it uses results_returned and the first-of-k dictionary line. The judge expects a mix of outcomes and cannot estimate without live runs. Borderline noted: on exact attachments the call reduces to a join; the stump rests on native linkage noise.

## Findings, ranked
1. Pass-1 hygiene finding closed.
2. Asks 2 and 3 are estimates (about +/-10 a week); a one-step tolerance would remove residual risk (optional).
3. Rubric criteria count not verified here.

## Next action for the author
Ship: proceed to stage 5 (target.zip from this rebuild, ledger row, card current).
