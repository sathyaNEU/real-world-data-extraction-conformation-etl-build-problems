# determinism-check report, task476 (architecture 5, pass 2), 2026-11-04

## Verdict
DETERMINISTIC (main call and all numeric asks)
**Disposition:** FIX_NOW (ask 2 cause wording only; failed gate: B, `answer_contradicts_files`)
**Stumping type:** mechanism: other (rating-shift detection and correction against discrete discharge measurements), stumping_family: analytical_non_defect (borderline), surface_read_dependency: no (borderline), sole_data_defect: no

## Why
Every graded figure reproduces from the bundle and every defensible literal reading lands inside the stated bands. The one finding is the cause answer in the deviation report (ask 2). It says the storm "left gravel on gauge BP-1's riffle control". No shipped file says gravel was deposited. The files license only that the storm shifted the control: logger and staff gage heights agree, and discharge after the storm is 13.8 to 18.0 per cent under Rating 7. A grader holding a solver to "gravel" would mark a correct answer wrong, so the cause is pinned only if the grader accepts any storm-induced control shift. Gate B: a distinctive term of the answer is in no input.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pre-storm visits vs Rating 7 | within 2.2% | -0.4, +0.2, +2.2, -1.6% | yes |
| Post-storm visits vs Rating 7 | 13.8 to 18.0% below | -14.5, -14.9, -13.8, -18.0% | yes |
| Stage shift (mean) | -0.0990 ft | -0.0971, -0.1006, -0.0994, -0.0986; mean -0.0990 | yes |
| Storm peak | 22:40 PST / 23:40 PDT 27 Jul | 6.604 ft at 22:40 PST | yes |
| Rows | 123 | 123 | yes |
| Deviation days / runs | 88; 29 Jul to 13 Sep, 21 Sep to 31 Oct | same | yes |
| Days by month | 3/31/23/31 | same | yes |
| 27 and 28 Jul means | 142, 277 | 141.6, 276.6 | yes |
| Aug / Oct mean | 46.1 / 27.0 | 46.05 / 27.02 | yes |
| 14 to 20 Sep mean | 55 | 55.2 | yes |
| Daily means (other days) within 2 cfs | listed values | worst gap 0.27 cfs | yes |
| Shortfall | 600 AF (+/-100) | 629.5 AF unrounded; 568 to 649 across all variants | yes |
| May / June volume | 18,800 / 9,000 AF | 18,804 / 8,994 (PST clock 18,841 / 8,959) | yes |
| Spring peak | 575 cfs 27 May 20:30 PDT | 575.25 cfs, 19:30 PST (same instant) | yes |

## Competing answers that survived
- Correction start time (peak, onset, 28 Jul 00:00, 29 Jul 00:00) gives identical daily means, 88 days and 629.5 AF. A start at the 29 Jul visit time gives 49.4 cfs on 29 Jul (one row outside the 2 cfs band, same 88 days, 623 AF). It is a weak reading, since the 26 Jul visit was still on the rating and the storm is the stated cause. Linear interpolation between the visits stays in band. Optionally state that grading assumes the shift applies from the storm.
- Shift vs ratio, mean vs fit: 568 to 649 AF, same 88 days and runs, daily means within about 1.2 cfs.
- A shift started at the 26 Jul visit gives 89 days. A correct reader would not do this, because the 26 Jul measurement is inside Rating 7's scatter.
- No correction (Rating 7 raw) gives zero deviations. This is the surface-read answer the stump targets, and it is not a survivor.
- PST vs PDT day boundary: 88 days either way, shortfall 630 AF.
- The 1.98347 AF per cfs-day constant is not in the files. It is a standard unit conversion and the +/-100 AF band absorbs any variation.
- None of these is an open fork on the main call.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 11 | yes |
| Formats | 3 or more | CSV, PDF, XLSX | yes |
| Large file | 25,000 rows or more | stage record, 27,360 rows | yes |
| Distractors | 2 or more, named in metadata.json, not labelled by file name | 3 (water temperature, generation, precipitation) plus the 2025 report as a stale-year read; no file name labels one | yes |
| Distractor behaviour | unused by the solution, relevant enough to weigh, none answers a graded quantity | none computes a flow; the 2025 report's 17,640 / 9,870 AF are last year's and are ruled out by their year | yes |
| Deliverables | 1 to 3, all in the golden, no format family required | 2 (xlsx, docx), both in the golden | yes |
| Asks | multi-dimensional, with unit and rounding | daily rows plus periods, cause, shortfall, volumes and peak; each states unit and rounding | yes |
| Prompt shape and rubric | identifiable shape, 25 or more criteria | ETL reconstruction of 123 daily rows plus report items; the criteria count comes from the generated rubric and is not visible to me, so I could not confirm it | not confirmed |
| Realism | nothing reads as LLM generated | the judge found operational artifacts with mixed clocks and a hydrographer's remarks, and no authoring disclosures | yes |
| Ask 2 wording | every answer licensed by the files | "gravel on the riffle control" is not in any file | NO (Gate B) |

## Gate G reconciliation
The thread's read: surface read is Rating 7 on the shifted stage record, which gives no deviation. The distractors (temperature, generation, precipitation) are not named as carrying the task. This matches the design note's analyst test, which files no deviation on Rating 7. The declared distractors are not too load-bearing, and no shipped artifact ranks the candidates wrongly. The thread flagged `surface_read_dependency` as borderline because the task overturns the reported read. It judges this a pass, since the rating is the licensee's own filed method and the shift is a fitted standard correction, not a planted defect. If a reviewer reads it as `planted_defect_flip`, route it to the portal. The design note's `sole_data_defect: none` and the thread's `no` agree. The note's parenthetical "gravel on the riffle control" is the same unlicensed phrase as in ask 2.

Gate H: domain pass (the swap test fails: a rating shift fitted to discharge measurements is a hydrographer's own record computation); layers pass (Layer 1 is the PST logger, split rating, 10-minute data; Layer 2 is judging and timing the shift); decisive_step analytical. The thread and the design note agree on all three. The thread's one flag is that the shift is a standard USGS method a strong solver may reach (`stumping` 1.3), so a solver that starts the shift at the visit date would still mostly land the call. The main thread weighs that against the ladder.

## Stump power (Gate F)
Good. The default path (Rating 7 as filed) ends on no deviation in 2026. Catching the shift needs the measurements set against the rating, then fitting the shift and timing it from the storm, then recognising that the 14 to 20 Sep pulse lifts the corrected flow above 50 cfs. A solver that applies a shift but starts it at the 29 Jul visit time still mostly lands the call. This is a landable call for a strong analyst, recorded for the main thread to weigh against the ladder.

## Findings, ranked
1. Ask 2 cause ("gravel on the riffle control") is not in any shipped file. Gate B, `answer_contradicts_files`. FIX_NOW.
2. Optional: state that the 29 Jul daily-mean grading assumes the shift applies from the storm, which closes the visit-time start.
3. Borderline: surface_read_dependency and stumping_family, which the portal could read as a planted-defect flip. No change needed.

## Next action for the author
Reword ask 2's cause in `submission.md` and the golden docx to: "the 27 July storm shifted BP-1's stage-discharge control, so Rating 7 overstated every later flow by 14 to 18 per cent while the plant held the rated setpoint". Drop "gravel on the riffle control" from the answer and from the design note's `Sole data defect` line, or keep it there only as a likely mechanism. No file in `target/` changes, so no model rerun.
