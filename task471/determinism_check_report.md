# determinism-check report, task471, 2026-10-20

## Verdict
DETERMINISTIC (main call), no SOLUTION_WRONG. Supplementary answers 2 and 3 (raw cut 49 and the rates that depend on it) are moderately fragile (Gate C).
**Disposition:** SEND_BACK
**Stumping type:** mechanism: planted_defect_flip (secondary etl_conformance / method_selection), stumping_family: surface_read_rejection, surface_read_dependency: yes, sole_data_defect: yes

## Why
Every load-bearing figure reproduced from the bundle (49 cut, five programs, all 16 rates, all 16 prior-year rows). The five-program list holds for any anchor correction of about 0.44 to 1.55 raw points, so the main call is forced. The call turns on correcting Arcwright's as-scored WA2 (0.245 points per read below the 2025 standard) from the validity papers. The judge reads that as a banned scaffold: a reported figure is wrong and the task is to flip off it. On clean scoring the task is routine equating (cut 52). Gate H decisive step: analytical, borderline planted. The judge's thread and the design note disagree on the Gate G label (see reconciliation).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| First attempts 25A / 26A | 3,035 / 3,215 | same (attempt history) | yes |
| WA2 shift per read | 0.25 (958 reads, 120 papers) | 0.245 pooled, 0.2505 paper mean (reads file + QC Validity papers) | yes |
| 2026 WA2 / anchor shift | +0.49 / +0.98 | same | yes |
| Raw 49 equated | 55.88 to 56.02 | 55.88-55.96 linear, 56.01 chained EP | yes |
| Raw 48 equated | 54.90 to 55.13 | 54.89-54.97, 55.13 chained EP | yes |
| Form 26A passing raw | 49 | 49 (table 56 -> 240) | yes |
| Five programs and rates (69.0, 58.1, 58.5, 61.6, 64.5); Delacourt 72.0 | as filed | same | yes |
| All 16 2025-26 rows; all 16 2024-25 rows | as filed | same | yes |
| Unadjusted anchor | cut 52, eight programs | same | yes |
| MC-only anchor | cut 46/47 | same; Eastridge off at 47 | yes |

## Competing answers that survived
1. Anchor correction: cut is 49 only if the anchor shift lies in about [0.84, 1.18] (cut 50 at 0.72; cut 48 at 1.18). Forward-regression calibration gives about 0.18 per read (cut 50); reverse regression about 0.29 (edge). The validity bias is not uniform by score on file (1 -> 1.15, 2 -> 1.88, 3 -> 2.56, 4 -> 3.61) and the papers were selected on two-read agreement. The list of five survives; the raw cut and the counts and rates in asks 2 and 3 do not. Closing rule: the prompt files no calibration method.
2. MC-only anchor (raw 46/47, three or four programs). Closed in the files only by Pellmore section 4 and the OAR memo representativeness criterion; dropping a drifting constructed-response item is also standard practice. Adequate, not airtight. Both stage-4 readers took this route.
3. 2024-25 link by name and birth date when the register ID has no history. Not filed (only suggested by the 2026 crosswalk). ID-only counts differ for every program (Ostrander 230 / 87.0 vs 243 / 87.7). Minor Gate E risk on ask 4.
4. The prompt says "by the June 2025 administration" while the deliverable uses a June 14, 2025 cutoff; the judge found it consistent with the filed data, no live fork recorded.
Settled and not live: first-attempt versus all-candidate samples (still 56), resolution-read shift (about 0.03).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 17 | yes |
| Formats | 3 or more | 3 (5 pdf, 9 csv, 3 xlsx) | yes |
| Large file | 25,000 rows or more | 250,260 (item responses) | yes |
| Distractors in metadata.json, none in a file name | 2 or more | 2 (BESL_ELI_Framework_2024.pdf, Arcwright_ELI_June2026_Administration_Summary.pdf); the judge's hygiene read finds the EPP directory also unused; file names do not label a distractor | yes |
| Distractor weighs but is ruled out | yes | not separately tested by the judge beyond hygiene; the thread did not name either as the surface read | not fully verified |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 32 figures across 16 programs; per cent to one decimal, whole completers | yes |
| Prompt shape and 25+ criteria | identifiable, 25+ | shape 10 (scorecard); 32 ask figures plus call and components exceed 25 on paper, rubric not generated here | yes (inferred) |
| Not LLM generated; goldens realistic | yes | judge found no authoring leakage; golden realism not rechecked here | yes (judge) |

## Gate G reconciliation
Judge: mechanism planted_defect_flip, stumping_family surface_read_rejection, surface_read_dependency yes, sole_data_defect yes. Design note: the Gate G strategy is "other (own:rater-severity-drift-on-a-constructed-response-anchor)" and "Not a plant: no document names the raters' shift, an adjusted anchor or a verdict". Note also says Gate G method_or_model_selection fits other builds, not this one. Mismatch: the note claims analytical trend-scoring; an outside reader names the as-scored Arcwright anchor the banned surface read and the shift the single data defect. This is the finding that most reliably predicts a send-back. The declared distractors (framework, administration summary) were not named as the surface read, so they are not too load-bearing; the load-bearing surface read is a non-declared, real input (Arcwright's reported WA2 scores). The Arcwright QC Notes line, the Validity papers sheet and the OAR memo each state that the WA2 validity papers are June 2025 responses with 2025 scores, which makes the correction easy to find and gives a reader a "planted-looking" signal (one stage-4 reader said so).

Gate H: domain pass (test equating is the field's own work); layers pass; decisive_step analytical, borderline planted (the answer turns on a built-in severity). Per the design note and the stage-4 readers, question 6 was answered "an analytical choice" by both readers, one adding "partly a planted-looking signal".

## Stump power (Gate F)
Both blind stage-4 readers failed: both took the drop-WA2 route (raw 47 and 46, four and three programs), both missed the five-program call and all 32 ask figures. That is strong stump evidence on paper. The weakness is the one the judge notes: discovery of the validity papers is signposted three times, so the difficulty rests on the computation and the anchor design, not on finding the data; and the readers' wrong route (drop WA2) is a defensible psychometric choice that the files close only through the representativeness criterion.

## Findings, ranked
1. Gate G: judge classes the decisive step planted_defect_flip / surface_read_rejection (banned scaffold); mismatch with the design note's analytical label. Send-back class.
2. Calibration unpinned: cut 49 holds only for anchor shifts of 0.84 to 1.18; a non-mean calibration gives 50. Asks 2 and 3 and the rates fork on it.
3. MC-only anchor is a surviving competing method closed by prose, not by a filed criterion in the prompt.
4. 2024-25 name and birth date link is unfiled (ask 4, minor).
5. Signposting of the validity papers in three places (QC Notes, Validity sheet, OAR memo) lowers the stump and invites the planted reading.

## Next action for the author
Redesign the decisive step per the judge's fix: either replace the drift-correction mechanism with consistent scoring across contractors and put the difficulty in a validated equating-design choice, or, if the build is kept, file the WHAT (the 2026 WA2 reads are to be put on the 2025 standard from the validity papers, and the 2024-25 name and birth date link) without filing the HOW, re-check the [0.84, 1.18] window, and re-run this check once.
