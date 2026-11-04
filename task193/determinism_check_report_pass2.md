# determinism-check report (pass 2), task193, 2026-11-04

Judge thread: one Sonnet thread, fresh unzip at /tmp/determinism-check-task193-pass2-1793771206/target/, verdict at /tmp/determinism-check-task193-pass2-1793771206/verdict.md. target.zip sha256 bb9d200b...774e68. The pass 1 report is untouched.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (two low-risk ask residuals, (b) and (d) below, stay open on graded figures; neither touches the call)
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Every committed figure reproduced from the shipped files. SAP section 4 defines background as groundwater the landfill has not affected; the gauging export plus the survey in force on each date show MW-1 below PZ-1 on 10 events and MW-2 below PZ-2 on 6, leaving 34/34/33 results and limits 38.2, 20.8, 68.3, so MW-6, MW-7, MW-9. The pooled-everything route gives 55.5, 34.8, 109 and MW-6 alone; MW-3 alone adds MW-10. Margins 12 to 16 per cent, call robust to every variant the judge tried.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| MW-1 / MW-2 / MW-3 reversed events | 10 / 6 / 0 | 10 / 6 / 0 (min abs head difference 0.11 ft) | yes |
| Background counts | 34 / 34 / 33 | 34 / 34 / 33 (50/50/49 before) | yes |
| UPL chloride, sodium, boron | 38.2 / 20.8 / 68.3 | 38.229 / 20.823 / 68.316 | yes |
| October results, 8 compliance wells x 3 | as filed | all matched | yes |
| Specific conductance, 11 wells | 584, 670, 574, 563, 533, 1096, 702, 591, 625, 682, 599 | same | yes |
| Purge gallons, 11 wells | 3.5, 3.0, 2.5, 2.1, 1.7, 2.6, 3.1, 4.3, 3.3, 3.2, 3.6 | same (raw 3.48 ... 3.60) | yes |

## Competing answers that survived
Main call: none. Asks (all in the fork table or ask sheet except where stated):
- (a) set at sampling, last set before the custody minute against last set before pump-off (MW-1 593 against 584, MW-2 680 against 670, 9 of 11 wells move): **closed.** FS-03 section 3 (shipped): "Collect the sample immediately after the last of those sets; the field readings reported with a sample are that set's." With the chain-of-custody collection minute this selects the last set before it. Ask sheet D8 records it as the deliberate primary device, with `checks.py` asserting the custody minute sits at least 30 s after the sample's set and at least 120 s before the next, so any minute convention picks one set.
- (b) purge counter read at the set against interpolated to the custody minute (MW-1 3.5 against 3.6): **open on a graded figure, low risk.** The note's closure is only an assertion ("no counter is read at the collection minute, so the purge ends at the counter of the set the sample was collected immediately after"), resting on FS-03 section 3's "that set's" readings. FS-03 section 2 says "until its sample is collected" from the counter, which a literal reader could interpolate. Not asserted to converge; at least MW-1 moves a cell.
- (c) UTC offset never written in the files: **closed by asserted convergence.** The note asserts only a five-hour local-daylight offset places every custody minute in its purge window (an hour later every sample follows its pump stop; read as UTC every sample precedes its visit). The offset is determined by alignment, so no second reading survives.
- (d) gallon conversion (3.785 L, controller counter is in litres, `controller_l`): **open on a graded figure, low risk.** No file defines the gallon and the design note's fork table has no row for it. US against imperial gallon (4.546 L) would move every purge figure. Closed in practice by convention (US site, US state agency), not by a shipped sentence.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files, formats, large file | 10+ files, 3+ formats, 25,000+ rows | 12 files; csv, txt, pdf, xlsx, json; ridgeline_edd 25,142 lines (25,141 rows) | yes |
| Distractors | 2+ in metadata.json, none named in a file name | 3 (gas probe csv, precip json, site-inspection xlsx), unlabelled in file names | yes |
| Distractor role | unused by solution, weighs, shipped fact rules out, none answers a graded quantity | gas, precip and inspection logs are not used by any graded figure; none reproduces a graded quantity | yes (judge and metadata) |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, svg), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 11 wells each; whole uS/cm at 25 C, gallons to one decimal, three significant figures | yes |
| Prompt shape and 25+ criteria | identifiable shape, 25+ | shape identifiable (per-indicator limits, per-well results, 22+ figures); the rubric is generated downstream and not in the task folder, so the count is not verified here | yes on shape, unverified on count |
| Not LLM-generated, goldens real | | judge found no authoring language, two lab layouts read as real Layer 1 mess; golden realism is a separate skill | yes |
| Prompt | one paragraph, question first, under 1,000 characters | 805 characters, no persona or bullets | yes |

## Gate G reconciliation
Thread: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card (`stump_class: analytical`, analyst_test, domain_test): estimand_identification, contamination of the comparison; the default path ends on MW-6 alone, golden MW-6/MW-7/MW-9. Match. The card's `mechanism` field is empty (None), a card housekeeping gap, not a mismatch. The thread names no declared distractor as the surface read; the three distractors play no part in the decisive step. Judge flagged the borderline that impacted samples could read as a planted defect; the note's No-decoy line answers it (no memo, flag or figure carries MW-6 alone, reversals are ordinary pumping results).

Gate H: thread `domain: pass`, `layers: pass`, `decisive_step: analytical`; the note's Three rules (domain test, swap fails, Layer 2 estimand identification, Not semantics, Not rule application with the enumerated reading family) agree. One note on rule application: the SAP files no clause about heads, and 20 enumerated alternatives split across three call-sets, so the thread's analytical classification is not the standard-method-by-default case.

## Stump power (Gate F)
Moderate to strong. The easy route files MW-6 alone; the right route needs each background sample tested against its own event's head relation and the datum change. The note's own paper ladder gives pair ceiling 33.5 (cracker 50.0 on the call, mirror 17.0 off it); the main call, not the asks, carries the stump. The asks add device-level misses (A1 2 of 11 and A2 0 of 11 for a call-landing solver who skips the field-log steps). Main thread weighs this against the ladder.

## Findings, ranked
1. (b) purge interpolation residual, graded figure MW-1 3.5 against 3.6, asserted but not closed by a shipped sentence.
2. (d) gallon definition absent from the pack and the fork table.
3. Card `mechanism` field empty.
4. Rubric criteria count not checkable from the task folder.

## Next action for the author
Optionally add a fork-table row and assert convergence for (b) and (d), or pin the prompt with "US gallons". Caution: the judge's suggested pin ("its field readings and purge volume at the sample's collection time on the chain of custody") would invite interpolation and worsen (b); a safer pin is "the set the sample was collected immediately after". Ship without either if the main thread accepts the residuals.
