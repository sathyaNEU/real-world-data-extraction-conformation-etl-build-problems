# determinism-check report, task234, 2026-10-31 (pass 2, stage 4 reship, target.zip d84a1971)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection (back-tested denominator estimator under a filed selection rule, with etl_conformance), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated thread (sonnet, medium) read only a fresh unzip of the bundle and the inlined blocks. FCP-2 s.2 to s.5 forces the escalation set. Tests are collapsed as filed. The week-3 denominator is the estimate whose back-test miss on week 2 is smallest. Every positivity-driven estimator tried (Poisson with trend, with and without the holiday weeks, positivity only, quadratic, OLS) escalates exactly Wexmoor's and Westmarch's six streams. They sit at 54.7 to 60.8 per cent; the lowest other stream is 87.4. Only estimators that lose the back-test (last week's report, held tests, constant, trend only; max miss 52.6 to 73.5 per cent) give a different grid, and the protocol's own criterion rejects them. Judge: no fix needed.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Week-3 tests, 29 streams | 80,671 | 80,671 | yes |
| Wexmoor / Westmarch week-3 tests | 3,128, 607, 1,234 / 1,943, 621, 1,454 | same | yes |
| Positivity | 33.1, 7.9, 9.6 / 23.3, 9.0, 17.0 | same | yes |
| Back-test max miss: fitted / held tests / last report | 7.8 / 52.6 / 54.0 | same | yes |
| Predicted tests | 5,714, 1,064, 2,219 / 3,514, 1,102, 2,391 | same | yes |
| Completeness | 55, 57, 56 / 55, 56, 61; others at least 87 | 54.7, 57.1, 55.6 / 55.3, 56.3, 60.8; others at least 87.4 | yes |
| Week-2 completeness, all 29 | 98.0 ... 47.4 ... 93.9 | all 29 match (Brandmoor 48.0/47.4/48.3 on L05 RSV version 2) | yes |
| Specimens, 10 laboratories | 2,850 ... 2,835 | all 10 match | yes |

## Competing answers that survived
- The clock of `received` is not stated in any shipped file. Read as UTC, week-2 completeness is 99.2 to 99.7 for 25 streams and 50.5 to 51.6 for Brandmoor, so Ask A (supplementary answer 2) depends on the inference. The coordinator confirms this is Ask A's device D8 and is kept as designed. Receipts precede `released_utc` by about 6 hours before the 19 Jan 06:00 migration, which is impossible in UTC, and the change log gives the instant. The main call is unaffected: every week-3 receipt precedes the cutoff under either clock.
- The estimator candidate set is open. The s.5 criterion plus the data (7.8 against more than 50 per cent) closes the outcome, not the method. No tried alternative changed a stream-level result.
- Positivity treats inconclusive as not positive. FCP-2 does not define it. Inconclusive is 0.2 per cent of results and moves no shown figure.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 10 | yes |
| Formats | 3 or more | csv, xlsx, pdf | yes |
| Large file | 25,000 rows or more | 211,361 rows | yes |
| Distractors | 2 or more in `metadata.json`, none labelled by file name | 4 named (ED ILI, state positivity, admissions, vaccination coverage); the file names carry no label | yes |
| Distractor behaviour | unused by the solution, ruled out by a shipped fact | count no laboratory's tests (judge, design note) | yes |
| Deliverables | 1 to 3, all in the golden | 2 (xlsx, svg), both present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 29-cell, 29-cell and 10-cell grids; 1 decimal, per cent, integer counts | yes |
| Prompt shape and rubric | identifiable shape, 25 or more criteria | shape 07 (grid of cells); 29 + 29 + 10 + the recommendation and chart cells exceeds 25 | yes |
| Reads as real work | no LLM tell | none seen by the judge; golden-realism handled earlier | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, family analytical_non_defect, surface read none, sole data defect none. Design note and card agree (analytical_non_defect, no surface read). The declared distractors are not the surface read, and the easy route (last week's report as denominator, 15 escalations) comes from the method, not from them. No mismatch.

Gate H: the thread says domain pass, layers pass, decisive step analytical. The design note's Three rules say the same (domain pass, layers pass, decisive step analytical, with No decoy, Not semantics and Not rule application each filed). The thread's analytical call rests on a back-test choice the data settle (7.8 against above 50 per cent), not only on a standard method. Landable-call caveat: a strong solver who runs s.5's check over positivity-conditioned models lands the call, so the stump relies on the solver not trying positivity. That is a paper-ladder point for the main thread, as the design note already argues.

## Stump power (Gate F)
Judge: good. The easy route (week-3 tests over last week's report) escalates 15 streams, 9 of them complete streams, against the correct 6. The week-2 receipt clock and Brandmoor's version-2 report add independent trap value to the asks.

## Findings, ranked
1. The design note is stale against the shipped bundle (cleanup only, no pack change). It says "11 files in four formats", "three distractors" and a "dictionary" that names the broker as the receipt stamp's writer. The bundle holds 10 files in 3 formats with 4 named distractors, and no dictionary file. The judge found the receipt clock unstated, so the note's D8 rationale ("the dictionary names the hub's broker") does not hold on the shipped pack. D8 stands on the pre-migration receipts preceding their releases, as the coordinator states. The note's Estimand section also lists 7 sources including a dictionary and a test code list; correct the counts and drop the dictionary reference.
2. The judge's optional hardening is to state the `received` clock once in the change-log entry. The coordinator keeps it as designed, so this stays open and the single reading remains an inference. It would need a rebuild and reship, and the decisive step is not touched.
3. The design note says the earlier judge round was architecture 2 round 1 DETERMINISTIC/APPROVE. This pass (reship cut d84a1971) agrees. The pass-1 report at 2026-10-17 was FIX_NOW (a dictionary pin), and the shipped pack has no dictionary, so that pin may have been dropped or realised elsewhere. Worth a look when the note is corrected.

## Next action for the author
Correct the stale counts and the dictionary mention in DESIGN_NOTE.md (10 files, 3 formats, 4 distractors, no dictionary). Then proceed to ship. No pack change is needed.
