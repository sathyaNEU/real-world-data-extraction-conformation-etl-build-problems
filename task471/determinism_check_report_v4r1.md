# determinism-check report, task471, 2026-10-20 (run v4r1, target.zip b6990395f2efabc2)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (judge), with one optional filing pin (see Findings)
**Stumping type:** mechanism: decomposition_attribution / method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Read literally, Article 14(2)-(3) plus audit report section 5 fix the estimand: register count less the summed audit share not living there among sampled persons like each registered person, rounded, compared with 5,000. The shipped sample, visits and histories separate the candidate partitions; the migration-career partition (current stay by earlier departure) gives nine. All 24 departure and death rows reproduce from the hub log, acknowledgements, events extract and non-resident records. No decisive fact is missing from the files.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Register persons, 24 municipalities | 126,655 | 126,655 (extract trailer) | yes |
| Not living there (results 20, 30, 40) | 206 of 12,000 | 206 of 12,000 (visits, last record) | yes |
| Never settled from abroad | 26 of 9,181 | 26 of 9,181 | yes |
| Settled, no earlier departure | 139 of 2,598 | 139 of 2,598 | yes |
| Settled after earlier departure | 41 of 221 | 41 of 221 | yes |
| Qualifying set | 9 named | same nine (Eekhorst 4947, Haverstede 4946, Hilderloo 4959, Koudenbeek 4947) | yes |
| Departures abroad 2025, 24 rows | golden | all 24 match | yes |
| Deaths 2025, 24 rows | golden | all 24 match | yes |
| Hilderloo stay-of-1-to-4 count etc. (CC3, CC4) | as filed | not individually itemised by the judge; the cell rates they feed reproduced | partial |

## Competing answers that survived
- Coarse partition (earlier departure kept, stay merged to short/long) gives eight, because Haverstede and Koudenbeek reach 5,000 or above. The judge treats it as thin but clean: a solver who tests the stay gradient (1 to 4 at 11 per cent, 5 to 9 at 5.5, under 1 at 3.9) will not merge. Merging only under 1 with 1 to 4 still gives nine. The shipped closure is report 5's "the respects that bear on it", with the audit as the test.
- Departures counted by sent year alone adds 2 to 3 per municipality (supplement column only, not the call). The spec column wording makes the intersection the literal reading; a minor Gate E risk.
- Flat 1.72 per cent (Dalmeer in), register-field cells (eight, wrong members), stay alone (six): all lose to the data, not open forks.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | 5 (csv, txt, pdf, xlsx, docx) | yes |
| Large file | 25,000 rows or more | events extract 292,603 rows; register 126,657 | yes |
| Distractors in metadata.json | 2 or more, none in a file name | register_coverage_pilot_2024.xlsx, waste_levy_households_20260101.csv; names do not label them | yes |
| Distractor relevance | unused, weighable, ruled out by a shipped fact | judge found both unused; pilot (other municipalities, other date) and levy (billing) are ruled out by their own contents. I did not recompute an arithmetic answer from either | yes (judge basis) |
| Deliverables | 1 to 3, all in golden | 2 (csv, png), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 24 rows by qualifies, departures, deaths; "every count as a whole number" | yes |
| Prompt | one paragraph, under 1,000 characters | 498 characters; shape 10 scorecard | yes |
| Rubric 25 or more criteria | 25 | not generated yet; 24 municipalities by three fields plus count and chart supply well over 25 by shape | yes (by shape) |
| Reads as real, not LLM generated | none | judge found no authoring or benchmark language; I did not independently read the documents | yes (judge basis) |

## Gate G reconciliation
The thread's mechanism (post-stratified estimate, method_or_model_selection), family (analytical_non_defect), surface_read_dependency (no) and sole_data_defect (no) match the design note (composition_mix, Gate G method_or_model_selection, no planted defect, no decoy). The card holds stump_class analytical but no mechanism fields of its own to compare. The surface read the thread names is the flat rate or the register-field rate, not the declared distractors (pilot, levy), so the distractors are not load-bearing. Gate G passes.

## Gate H reconciliation
Thread: domain pass, layers pass, decisive_step analytical (estimating register over-coverage by post-stratifying a field audit). Card domain_test and the note's Three rules say the same, and the analyst test (default path files eight, the career strata file nine) is the thread's own competing-answer finding. No mismatch. One caution for the main thread: the judge reached the golden by testing candidate partitions on the audit (a selection the data settles), so this is a method-selection call, which the blind readers measured as landable (below).

## Stump power (Gate F)
Judge's line: high (flat rate or register fields fail; three named municipalities flip). Measured counter-evidence from the coordinator: both stage 4 scored isolated readers on the same target.zip landed the call (score_reader exit 1 each, 0 of 48 ask figures). Architecture 4 is therefore spent on Gate F whatever this verdict says, and the judge's "high" does not outweigh the readers. The call is a textbook route a strong solver takes once the event history is rebuilt (stumping 1.3). The asks gave the readers 0 of 48 figures, so the exposure is on the call, not the asks.

## Findings, ranked
1. Gate F: both scored readers landed the call; the architecture is spent (coordinator record). Decision for the main thread, not this judge.
2. Optional filing pin: the departures-in-2025 reading (event date and sent date both in 2025, CET) and a sentence naming the cell unit without naming the career split, to remove the coarse-partition fork. Must file the WHAT, never the HOW, so as not to turn the decisive step into rule application.
3. Judge did not itemise CC3/CC4 per-municipality counts; the cell rates they feed reproduced.

## Next action for the author
Treat Gate F as failed on the readers' measurement and decide re-root or redesign of the stump before shipping; if the judge's optional departures pin is applied, restate it as a population and window only and re-run the generator checks.
