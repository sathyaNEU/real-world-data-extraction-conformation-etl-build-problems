# determinism-check report, task476 (architecture 5), 2026-11-04

## Verdict
DETERMINISTIC, plus SOLUTION_WRONG (minor: one cell and one rounding statement).
**Disposition:** FIX_NOW
**Failed gate (section 6):** Gate A (a graded figure does not recompute from the solution's own stated step: "0.10 ft" gives 276 cfs for 28 July, the golden says 277; `solution_incorrect`, minor). Residual Gate C/E exposure on the per-day cfs asks only (correction form and the shift's effective time are unfiled); the main call, periods, 88 days and 600 acre-feet are not exposed. Gates H, G, B, D and F pass.
**Stumping type:** mechanism: method_or_model_selection (rating validation against gaugings, stage shift), stumping_family: analytical_non_defect (borderline), surface_read_dependency: no (borderline), sole_data_defect: yes by the thread's clean-data test (see Gate G reconciliation)

The judge thread ran as a single isolated pass (scratch /tmp/determinism-check-task476-v5-092745, fresh unzip, verdict.md there). It was spawned by the main session because this runtime has no Agent tool; the brief is judge_brief.md in the same folder.

## Why
The main call is forced by the shipped files. Rating 7 (register table plus the 2023 memo's high-water equation) applied to the stage logger, shifted one hour to local PDT, keeps every July to September day at or above 53.8 cfs. The four post-storm measurements (29 Jul, 25 Aug, 16 Sep, 6 Oct) sit 11.7 to 17.4 per cent below Rating 7, the four earlier ones within 0.4 per cent, and a constant stage shift of about -0.0986 ft fits all four with residuals under 1 cfs. On that relation the deviation days are 29 Jul to 13 Sep and 21 Sep to 31 Oct, 88 days, and the set and the met flags are identical under every correction tried (stage shift from the peak, from 28 or 29 July, ratio, prorated). The shortfall is 562 to 642 acre-feet across variants, all 600 to the nearest 100. May and June volumes and the spring peak reproduce, and are insensitive to PST versus PDT day boundaries.

The defects are on the solution side: the blocks state a rounded "0.10 ft" correction while the golden used the unrounded fit, and the per-day whole-cfs cells depend on a correction form and effective time that the prompt and files do not pick.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Table vs equation | n/a | register table = 22(GH-0.8)^2.3 within 0.005 cfs | yes |
| Pre-storm differences vs Rating 7 | within 0.4% | +0.2, -0.3, +0.4, +0.4 % | yes |
| Post-storm differences | 11.7 to 17.4% below | -14.4, -15.5, -11.7, -17.4 % | yes |
| Stage correction | 0.10 ft | -0.096, -0.105, -0.099, -0.095 (mean -0.0986) | yes, unrounded |
| August / October flow | 46.1 / 27.0 cfs | about 46.0 to 46.1 / about 27.0 | yes |
| Deviation days | 88 (3/31/23/31) | 88, same split | yes |
| Periods | 29 Jul to 13 Sep, 21 Sep to 31 Oct | same | yes |
| Rating 7 alone lowest day | 53.8 cfs | 53.8 (Jul to Sep), 32.8 (Oct) | yes |
| Shortfall | 600 AF | 622 to 642 (shift variants), 562 (ratio) | yes, rounds to 600 |
| 28 July cell | 277 cfs | 276.4 with 0.10 ft, 276.7 with -0.0986 | only with the unrounded shift |
| May / June volumes | 18,800 / 9,000 AF | 18,804 / 8,994 (PST days 18,841 / 8,959) | yes |
| Spring peak | 575 cfs 27 May 20:30 PDT | 575.25 cfs, same date either clock | yes |
| Row count | 123 | 123 | yes |
| Storm peak | late 27 Jul | 6.604 ft 22:40 PST (23:40 PDT) | yes |

## Competing answers that survived
None on the main call, periods, day count, shortfall, May/June volumes or peak. On the per-day cells only:
- Correction form: stage shift (golden) against flow ratio x0.853 differ on 40 of 123 whole-cfs cells (pulse days 83 to 84 against 80 to 81, October 27 against about 28). The shift fits better and the monitoring plan's "standard USGS methods" use shifts, but no sentence in the prompt or files picks the form.
- Effective time of the shift: from the storm peak (golden) against 27 Jul 00:00 (130 for 27 Jul against 142), 28 Jul 00:00 (279 for 28 Jul) or 29 Jul 00:00 (297). Only the 27 and 28 July cells move; both days are "met" under every reading.
- 28 July: 276 with the stated "0.10 ft", 277 with the unrounded fit.
- Clock (PST against PDT days): 88 days either way, 623 against 624 acre-feet.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 11 | yes |
| Formats | 3 or more | csv, pdf, xlsx | yes |
| Large file | 25,000 rows or more | bp1_stage_2026.csv 27,360 rows | yes |
| Distractors | 2 or more named in metadata.json, none labelled by file name | 3 (water temperature, daily generation, precipitation); names carry no label | yes |
| Distractor role | unused, weighs, none reproduces a graded quantity | none carries flow or rating; precipitation corroborates the storm but answers nothing graded | yes |
| Deliverables | 1 to 3, all in golden, no format family | 2 (xlsx, docx), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 123-row daily record plus periods, causes, shortfall, May/June volumes, peak; "whole cfs", "nearest 100 acre-feet" | yes |
| Prompt | one paragraph, under 1,000 chars, no data-held count | 618 chars, none | yes |
| Rubric | 25 or more criteria, prompt shape identifiable | shape 17 (card); the rubric is portal-generated, so not verifiable here, the 123 cells and periods give the volume | not checkable, expected yes |
| Reads as real | no LLM tells, goldens read as work products | thread found none (Doppler notes, greasing log, signed 2025 report, datum details) | yes |

## Gate G reconciliation
Compared against the card and DESIGN_NOTE.md, read only after the thread returned.
- mechanism: thread method_or_model_selection; card gate_g signal_vs_noise_or_hold (redrawn from method_or_model_selection on 2026-11-04 for a window clash with task462 v2), stump_strategy forecast_method_backtest, notes "measurements test the published rating as a back-test does a method". The thread reads the mechanism as method selection, which is the card's earlier label. This is a label mismatch: the redraw changed the card's gate_g without the build changing, and the note's own text (relation chosen by measurements) is method/model selection. Finding: correct the card's gate_g to match the build, or defend signal_vs_noise_or_hold in the note. A mismatch is the finding that most reliably predicts a send-back.
- stumping_family: thread analytical_non_defect; card stump_class analytical. Match.
- surface_read_dependency: thread no (borderline), matching the note (nothing planted, no certified replay). The thread did not name the declared distractors (temperature, generation, precipitation) as carrying the task, so they are not too load-bearing.
- sole_data_defect: thread yes by the clean-data test, while also saying no reported figure is wrong and the shift is a real change in the shipped measurements. The card's analyst_test is written on clean truth and says the easy route lands on no deviation because the rating is stale, not because any datum is wrong. Architecture 4 was spent on exactly this question, so the main thread should weigh it: the staleness here is physical and the measurements show it, but a reviewer who reads a stale published rating as a "defect" will class it that way. Gate H still passed.
- Gate H line: domain pass (stage-discharge record computation held to gaugings for licence compliance; the swap test fails), layers pass (Layer 1: PST logger against local days, table plus equation split at 4 ft; Layer 2: rating validation and shift), decisive_step analytical. Matches the note's Three rules and the card's analyst_test and domain_test.
- Weakness the thread named: the 29 July remark "Control riffle reworked by the 27 July flood" and the 45.7 against 53.4 cfs gap nearly announce the shift (semantics-adjacent). Choosing and fitting the correction is analysis, so the decisive step stands.
- Gate G (no shipped artifact ranks the call wrongly): pass. The release log's 54 cfs setpoint and the 2025 report are true on their own terms; difficulty survives deleting every wrong number.

## Stump power (Gate F)
Moderate. A solver who applies the register's "Rating in use: Rating 7" files no deviation, a wrong answer, so the stump sentence can be written. But a strong solver who reads the visit file sees the post-storm gap and the remark, and a textbook USGS shift is a standard route a strong solver takes (stumping 1.3). The thread did not class the decisive step analytical merely because the method is standard: it reached the golden by choosing and fitting a correction the data had to settle, and the thread's own hand-fit was needed to separate shift from ratio. The main thread should weigh against the note's ladder (rung 0 dies to four measurements). The separating work is the per-day cells (form, fit, cutover), which already carry weight in the asks. The note's ladder supports one of the top two being off the call only if the post-storm comparison is not made by default; the thread judges that a competent run will probably make it.

## Findings, ranked
1. Solution blocks state the correction as "0.10 ft", which gives 276 for 28 July, not the golden's 277 (Gate A, minor). The design note's decisive-step line repeats "0.10 ft"; its stump sentence says 13 to 18 per cent where the components say 11.7 to 17.4.
2. Per-day whole-cfs cells depend on the correction form (40 of 123 differ) and the shift's effective time (27 and 28 July) that no filed sentence picks. Main call unaffected. Filing the shift form in the prompt would file the HOW and turn the decisive step into rule application, so it must not be filed; the fix is a tolerance or an unrounded restatement.
3. Card gate_g (signal_vs_noise_or_hold) against the thread's method_or_model_selection mechanism (label mismatch).
4. sole_data_defect read as yes by the thread's clean-data test; borderline, to be argued in the note given architecture 4's fate.
5. The field remark and the visit gap nearly announce the shift (stump power).

## Next action for the author
Restate the correction in the solution blocks (and the note) as the unrounded fitted stage shift, about 0.10 ft (-0.0986 ft), applied from the storm's peak, so 28 July reads 277, and align the stump sentence's range to 11.7 to 17.4 per cent. Then correct the card's gate_g to the build's mechanism and add to the note's Three rules a line answering the sole_data_defect reading. The prompt, pack, 600 acre-feet, periods, 88 days, May and June volumes and 575 cfs peak stay byte-identical, and no rerun is needed. If the rubric compares per-day cfs cells, grade with a 1 to 2 cfs tolerance (wider for 27 and 28 July).
