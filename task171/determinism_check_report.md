# determinism-check report, task171, 2026-10-27

Pass history, one line each: pass 1 (zip 5c3c5b81) NOT_DETERMINISTIC on the forecast decimals, fixed by filing the below-limit rule in SAP 6.8, a time_zone column on the site list and the model form in charter 4. Pass 2 (zip e3c93a97) NOT_DETERMINISTIC on ask A from per-review severity changes, fixed by carrying severity per event and clarifying SAP 6.3. Pass 3 (zip 8ef4cd41) DETERMINISTIC with FIX_NOW on the unfiled adverse-event onset convention, the handset trace and the unreproduced scope of critical components 1 and 3, fixed by SAP 6.3 filing that each review's record shows the event as it stood then (the latest record its current form), critical components 1 and 3 stating their scope, and the handset trace left to the data. Pass 4 below (zip 4a85c214, matches the current target.zip) is the verdict of record.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The charter leaves the exposure measure open, but the shipped concentrations separate the candidates: the remitter to non-remitter geometric-mean ratio rises from 1.02 (week 4 pre-dose) to 2.26 (week 8) and 3.12 (week 12), so later troughs carry outcome-dependent clearance. Only the week-4 pre-dose concentration is usable; on it remission is flat and the forecasts are 40.7, 40.9 and 41.0, so 300 mg is forced. Every committed figure, main and supplementary, reproduced. No SOLUTION_WRONG.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Post-start pre-dose samples set aside, week 4 / week 8 | 15 / 20 | 15 / 20 | yes |
| Analysis set | 455 of 480 | 455 of 480 | yes |
| Ratio wk4 / wk8 / wk12 | 1.02 / 2.26 / 3.12 | 1.0156 / 2.2559 / 3.1235 | yes |
| Quartile remission | 43, 37, 39, 45 | 43.0, 36.8, 38.9, 44.7 | yes |
| Forecasts 300/600/900 | 40.7/40.9/41.0 | 40.71/40.88/40.98 | yes |
| 300 mg gap, concentration only / with weight and Mayo | within 0.43 | 0.43 / 0.26 | yes |
| Serious-infection patients | 12 / 7 | 12 / 7 | yes |
| Infusion-related reaction patients | 32 / 13 | 32 / 13 | yes |
| SI per 100 py | 11.0 / 14.7 | 11.05 / 14.74 | yes |
| ADA incidence wk 4/8/12 | 2.5/5.6/8.7; 0.4/1.3/2.2 | same (12/471, 26/462, 39/450; 1/238, 3/230, 5/223) | yes |
| E-diary remission wk 6/8/10 | 133/196/208; 17/32/35 | same | yes |

## Competing answers that survived
None flips a committed main answer. On the supplementary asks only:
- Each AE record as its own event: serious infection patients 15 / 9, infusion-related reaction patients 44 / 19. First-record onset: 15 / 9 and 43 / 19. Closed by SAP 6.3 (latest record is the event's current form); the judge notes the chaining remains inferred rather than stated outright.
- Dropping the unknown diary registrations: dovikizumab 131 / 191 / 202, placebo 15 / 30 / 33. Closed by handset ownership in the data (unique predecessor), not stated in a file.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10+ / 3+ / 25,000 rows | 20 / csv, pdf, xlsx / e-diary 67,252 rows | yes |
| Distractors in metadata.json | 2+, none in a file name | 3 (hv101 PK summary, concomitant medications, efficacy topline extract), none labelled by file name | yes |
| Distractor relevance and ruling out | unused, weighable, ruled out by a shipped fact | topline extract (local reads, 203 remitters against 214 at lock) judged a correct distractor; the judge named none as the surface read | yes |
| Deliverables | 1 to 3, each in the golden | 3 (docx, xlsx, png) | yes |
| Asks | multi-dimensional, unit and rounding stated | arm-by-visit grids, decimals and whole counts stated in the prompt | yes |
| Prompt shape and 25+ criteria | identifiable, 25+ | shape 07 (grid of cells), about 18 xlsx cells plus call, components, chart parts, files; rubric not shipped, count not verified | likely |
| Reads as real, not LLM generated | yes | operational exports, coherent dates, no authoring disclosure | yes |

## Gate G reconciliation
Judge: method_or_model_selection, analytical_non_defect, surface read no, sole data defect no. It did not name the declared distractor as carrying the task. The mechanism (exposure measure under reverse causation, clearance falling as colitis heals) matches the design note's stump and domain test. No mismatch.
Gate H: domain pass, layers pass, decisive_step analytical. Matches the design note's three-rules lines.

## Stump power (Gate F)
Moderate to good. Week-8 and week-12 troughs give steep relationships (29.6 / 42.5 / 50.6 and 27.7 / 43.1 / 52.5) and file 900 mg after a clean read; only a solver who tests whether concentration depends on response avoids it. The decisive step is an estimand and exposure choice, not a field reading or an executed procedure, and the judge did not class it as a textbook landing. The cleaning (15 and 20 late samples, units) does not move the call. The main thread weighs the ladder as usual.

## Findings, ranked
1. Residual: the charter does not name the exposure measure; the judge treats a wrong choice as a reasoned analytical error, which is the intended stump, not an open fork.
2. Optional pins (not required): state the AE linking by patient and preferred term while ongoing, and the handset continuation for an unlisted registration. Either would reduce supplementary-ask fork risk without touching the stump; the second would be filing a trace the data already forces.
3. Cross-batch fingerprinting was not part of this review.

## Next action for the author
None required for determinism. Proceed to ship with the card and the pre-ship check.
