# determinism-check report, task473, 2026-11-02 (pass 4, the single re-judge of a FIX_NOW)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judged cut: target.zip md5 b01d61394f12389322e0578cb21baf1e (the final cut, which drops the court extract's counts column). The earlier spawn brief named md5 c065f483...; the coordinator refreshed the scratch bundle to the final cut before the thread ran, and the folder's target.zip carries the final md5. Verdict file: /tmp/determinism-check-task473-pass4/verdict.md.

## Why
The main call is forced by guidelines 2.2 to 2.4 and manual 3.1 and 4.2: 30-day deaths by crash county, drivers as defined, the fully-testing agencies named in the manual, and a county rate against 0.60. It reproduced to the stated rounding (Tanager 65.83 deaths, 0.6588, so 0.66). All 28 court figures reproduced under the golden linking rule (a dismissal followed on the same day by a new case with the same court, offense date and agency: 268 links, none at 1 to 30 days after the dismissal). The pass-3 forks (b) lead charge and (c) any later same-key case no longer split the answer within the shipped data: a dismissal linked to a later case filed within 1 to 30 days does not exist, and the lead-charge condition no longer differs from the plain rule (all 268 links are DUI to DUI). The thread's residual risk: no shipped sentence states that a person is identified by dismissal-then-refile on one day, so the link is closed by the data, not by a filed sentence (see Competing answers).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Aldous deaths / rate | 32 / 0.52 | 32.00 / 0.5198 | yes |
| Brisbin | 59 / 0.54 | 58.83 / 0.5384 | yes |
| Corwin | 60 / 0.71 | 60.00 / 0.7097 | yes |
| Delmont | 79 / 0.51 | 79.00 / 0.5099 | yes |
| Fairlee | 90 / 0.45 | 90.00 / 0.4492 | yes |
| Hatchell | 85 / 0.68 | 84.80 / 0.6794 | yes |
| Keswick | 78 / 0.34 | 78.07 / 0.3397 | yes |
| Kittredge | 43 / 0.57 | 43.12 / 0.5697 | yes |
| Lanier | 51 / 0.54 | 51.22 / 0.5396 | yes |
| Ossian | 54 / 0.68 | 54.12 / 0.6797 | yes |
| Pruett | 102 / 0.55 | 101.87 / 0.5497 | yes |
| Renwick | 67 / 0.38 | 66.75 / 0.3798 | yes |
| Stroud | 57 / 0.41 | 57.25 / 0.4098 | yes |
| Tanager | 66 / 0.66 | 65.83 / 0.6588 | yes |
| Certified list | Corwin, Hatchell, Ossian, Tanager | same; nearest below Kittredge 0.570 | yes |
| Catch rates (full-testing agencies) | 28.6% and 88.9% | 20/70 and 72/81 | yes |
| Tanager excess untested impaired | 21.0 | 8(3.5-1) + 8(1.125-1) = 21.0 over 87 untested survivors (p = 0.2414) | yes |
| Step 3 RMS miss | 1.1 vs 3.4 | 1.14 vs 3.43 (band-blind pooled 3.86) | yes |
| 14 offense counts and 14 conviction per cents (ask 2) | see submission | all 28 reproduced under the golden rule; exact ties Aldous 92/160 = 57.5, Fairlee 250/400 = 62.5, Hatchell 204/340 = 60.0 | yes |

Thread's supporting checks: crash files 945 + 987 + 983 crashes, all 60 former agency codes map to the directory, 3,131 fatal persons all within 30 days (six non-fatal rows with death dates 32 to 68 days out are excluded and none involves an impaired driver), 87 hit-and-run rows with age 999 or blank dropped, 3,578 drivers (1,631 killed, 1,947 surviving), 937 of 937 surviving drivers tested at the fully-testing agencies against 144 of 1,010 elsewhere. No figure sits within 0.0003 of a rounding edge. Court file: 31,404 rows, unique (court, case_number), 4,736 cases with a DUI lead charge and 2025 offense date, no disposition after 28 Feb 2027.

## Competing answers that survived
The thread's wording: "nothing in the shipped files states that a person is identified by a dismissal-then-refile on one day." Readings that move every county are open at the level of sentences and closed only by the data:

| Reading | Result vs golden |
|---|---|
| One per case number (no linking) | all 14 move (Aldous 170, 54.1) |
| Golden rule; same without agency; link any later case of any charge; link within 3, 7 or 30 days after the dismissal | matches (268 links; no same-key DUI case 1 to 30 days after a dismissal; no DUI dismissal linked same-day to a non-DUI case) |
| Dismissal linked to any later same-key DUI case filed after the dismissed case was filed (even before it was dismissed) | 333 links; all 14 move (Aldous 159, 57.9; Keswick 511, 66.1; Tanager 409, 63.1) |
| Same, without agency | all 14 move (Aldous 156, 59.0; Keswick 487, 69.4) |
| Collapse all same court, offense date and agency DUI cases, last case | all 14 move (Aldous 149, 56.4; Keswick 420, 66.9; Tanager 355, 62.3) |
| Collapse, first case | all 14 move (Aldous 149, 55.0; Keswick 420, 61.0) |
| Collapse, any conviction in group | all 14 move (Keswick 420, 71.4) |
| Collapse by court and offense date only | all 14 move (Keswick 259, 68.7) |
| Dismissed DUI linked to a later non-DUI case and the prosecution dropped | 2 move (Brisbin 334, 63.5; Kittredge 191, 58.6); if the prosecution is kept, nothing moves |
| Drug charge 42-1201(3) excluded | all 14 move (Aldous 154, 57.8; Keswick 494, 64.2); closed by guidelines 3.1 "alcohol or drugs, MSC 42-1201" |
| Drug conviction not counted | all 14 move (per cent only; Aldous 55.6); closed by 3.1 |
| Amended-charge pleas to reckless driving counted | all 14 move (per cent only; Aldous 70.6); closed by "conviction for impaired driving" |
| Deferred prosecutions counted | all 14 move (Aldous 62.5); closed by "conviction" |
| Window: filed in 2025 instead of offense in 2025 | all 14 move (Aldous 162, 58.0); closed by "committed in 2025" |
| Disposition strictly before 28 Feb 2027 (3 dispositions fall on that day) | 2 move: Fairlee 62.5 to 62.25, Pruett 54.9 to 54.6 (n unchanged); inclusive is the natural reading of "by that date" |
| Counts weighting | not available: one lead charge per case, no count field |

The thread closes the linking forks by three facts: (1) in the 62 extra links of the "any later same-key case" reading the second case was filed before the first was dismissed (gap -4 to -412 days), so it is a different matter, not a refile; (2) same-key DUI pairs remaining after the golden linking occur 674 times against 605 expected for independent arrests by the same agency on the same date, which fits distinct people; (3) the dismissal date equals the refile date in 268 of 268 links with none at a 1 to 30 day gap, a clean signature and not a tunable window.

Main-call method forks (guidelines 2.2 leaves the method open; the data separate the candidates, no back-test is filed): fully-testing set = State Patrol only gives the same list; agency-level untested probability gives the same list; one band-blind arrest rate (61% pooled) gives Brisbin 0.680, Corwin, Hatchell, Ossian, with Tanager at 0.553; one state-wide untested probability gives Corwin, Hatchell, Ossian, Pruett 0.635, with Tanager at 0.522; untested drivers taken as sober gives Tanager 0.450, not defensible against 2.2's "whether or not that driver was tested". DVMT on 365 days or 1,095 days moves no rounded rate. Counting deaths beyond 30 days moves nothing.

## Spec gates
Checked by me against the unzipped bundle and metadata.json.
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | csv, xlsx, pdf | yes |
| Large file | 25,000 rows or more | aoc_criminal_traffic_cases_2025_2027.csv, 31,404 rows | yes |
| Distractors named, none labelled by file name | 2 or more | dmv_licensed_drivers_by_county_2025.xlsx, fcc_2026_preliminary_crash.csv, both named in metadata.json; neither file name says distractor | yes |
| Distractors unused yet weighing | | licensed drivers (another denominator) and 2026 preliminary extract (another window); neither is on the solution path; the thread did not name either as a surface read | yes |
| Deliverables | 1 to 3, all in golden | 2 (CSV, PDF), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | | 14 counties by deaths, rate, offenses, per cent; rounding in the prompt (rates two decimals, deaths and offenses whole, per cents one decimal) | yes |
| Prompt shape, rubric 25 or more criteria | | shape 01 with a threshold for a cap named in metadata.json; the rubric is generated and was not inspected by me; the 28 gradable graded figures plus the list and chart exceed 25 | yes (rubric file not read) |
| Reads as real, not LLM generated | | thread hygiene PASS; no authoring language in the files; dates coherent with the 1 May 2027 certification | yes |

## Gate G reconciliation
Thread: `mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Card: `stump_class: analytical`; the card's analyst_test names the same easy route the thread found (one share of unarrested drivers, certifying Corwin, Hatchell, Ossian and Pruett), and the design note names the same wrong certifications (Pruett for Tanager; Brisbin for Tanager under one catch rate). No mismatch. The declared distractors are not the surface read carrying the task, so no finding on distractor load. Gate G classification: pass (no shipped artifact ranks the counties wrongly, the difficulty survives deleting every wrong number).

## Stump power (Gate F)
Real stump power on the main call: a strong solver who cleans the data and reads every rule can land on {Corwin, Hatchell, Ossian, Pruett} (state-wide share), {Brisbin, Corwin, Hatchell, Ossian} (band-blind arrest rate) or {Corwin, Hatchell, Ossian} (untested taken as sober). The shipped text does not announce the band-specific county rate. The thread reached the golden by testing four estimators against the data, not by applying a filed method, so this is not the textbook-route case. The court ask adds an independent layer: counting case numbers is wrong in all 14 counties. The design note's older figures (294 refile pairs, 31,430 rows) differ from the final cut (268 links, 31,404 rows); the ladder should be checked against the final cut by the main thread.

Gate H line: `domain: pass`, `layers: pass`, `decisive_step: analytical`. The field's own problem is estimating unobserved alcohol-impaired involvement from selective testing; Layer 1 is the two crash forms, former agency codes and DVMT units; the easy routes (recorded BAC only, one pooled arrest rate) do not follow from misreading a field. Design note's `## Three rules` carries the same classification.

## Findings, ranked
1. Residual, low: the person link in the court ask (dismissal then same-day refile) is not stated in any shipped sentence; it is closed by the data only. The alternatives that move every county are looser readings that the shipped data argue against. Not a defect per the thread.
2. Residual, low: "by 28 February 2027" read strictly (before) moves Fairlee 62.5 to 62.25 and Pruett 54.9 to 54.6; inclusive is the natural reading.
3. Residual, named: main-call estimator choice is closed by out-of-sample error, not by a filed criterion (guidelines 2.2 leaves the method open); the competing estimators give different lists, but the data separate them.
4. Note: submission.md step 6 still describes the link as "same offense date and arresting agency", which is the reading the thread reproduced; it makes no claim about the lead charge. No change needed.

## Next action for the author
None required; proceed to ship. Optional, the author's call: pin the person link in guidelines 3.1 or the court notes (the thread's example, "a case dismissed and re-opened for the same offense is one prosecution"), which would close the ask 2 fork but make ask 2 easier.
