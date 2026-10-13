# determinism-check report, task229, 2026-10-13

**Cut note.** The isolated judge thread ran on the 22-station cut (unzip at /tmp/determinism-check-task229-75970/target/, brief judge_brief.md). The main session then made one fix pass the thread did not see: a 23rd station (C124 Merrin Creek near the mouth, below the ungauged Vardy River, holds grade B), a dictionary replaced_by line closing the Mattin Creek soft fork, four realism rewrites, and the card's gate_g relabelled to forecasting. The design note, card, metadata, prompt (now "23 stations") and the shipped target.zip (byte-identical to target/, checked by diff) describe the final cut. The thread's recomputations of the 22 common stations, the 12 station-day counts and the 22 gauging means carry over; C124's own cells (within 1.0 per cent every month, 1.5 at the corridor worst) and the dictionary line were NOT seen by the thread and rest on the generator's assertions (1,696) and verify.py (313 checks) only.

## Verdict
DETERMINISTIC (thread verdict on the 22-station cut; no SOLUTION_WRONG)
**Disposition:** APPROVE (no FIX_NOW; the thread's one optional fix is already applied in the final cut)
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Read literally, the standard (s3, s4) grades a station-month on the published monthly mean against the true monthly mean (5 per cent) plus the 1.5x extrapolation rule against the rating book's gauged top; the dictionary fixes published discharge as the rating at the day's mean level; the operating plan and outlook fix the peaking windows, minimum release, ramps and flows. Executed word for word the error at C104, C105, C112, C113 is 14 to 32 per cent low in every peaking month, outside 5 per cent under every ramp convention tried; Sable Creek is the only extrapolation case. All three committed answer sets reproduced.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| C105 Feb shortfall (minimum) | 14.4 per cent | -14.4 (1-minute day simulation, rating book, outlook, plan) | yes |
| C104 Jul shortfall (maximum) | 32 per cent | -32.3 | yes |
| C112/C113 June | 0 (continuous generation) | 0 through June, -18 to -32 from July | yes |
| Sable May/June flows vs 1.5x gauged top | 8.65, 9.44 vs 4.21 | consistent with the book's gauged top | yes |
| Station-days Oct 2025 to Sep 2026 | 658, 643, 657, 650, 592, 662, 636, 673, 655, 675, 674, 653 | same (22-station cut) | yes |
| Gauging mean differences | 22 values, 1 dp | all 21 non-Mattin match; C122 -1.99 only when C110 and C122 pooled | yes (pooled reading) |
| C124 within 1.0 per cent every month | 1.0 | not seen by thread | no thread check (generator and verify.py only) |
| Station-day counts and C122 mean on the 23-station cut | unchanged | not re-run by thread | carried over, unverified by thread |

## Competing answers that survived
- Thread-raised soft fork, Mattin Creek (C110 to C122): reading (a) mean C122's 5 gaugings only (-1.1), (b) count C110 and C122 as two stations on 4 to 8 June (June 660). Closed in the final cut by the dictionary line "the closed number's daily rows and gaugings are that station's" and by SF16. The thread did not see the closing line; I confirmed it is in the shipped data_dictionary.csv.
- New in the final cut (not judged): a solver flagging every station below a peaking plant would flag C124 wrongly; the design closes it by C124 holding within 1.0 per cent. Not a fork, a discriminator.
- No surviving fork on the main call.

## Spec gates (checked by me against the final unzipped bundle)
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 14 | yes |
| Formats | 3+ | 4 (csv, pdf, xlsx, docx) | yes |
| Large file | 25,000+ rows | daily_records 39,930 rows | yes |
| Distractors | 2+ in metadata.json, none labelled by file name | flood_frequency_update_2025.pdf, water_quality_grab_samples_2026.csv; names neutral | yes |
| Distractor weight | unused, relevant, ruled out by a shipped fact | flood update covers unregulated stations only and is "not analysed" below plants; WQ samples are chemistry. Neither answers a graded quantity. field_visits is an unnamed third extra | yes (weak but acceptable) |
| Deliverables | 1 to 3, all in golden | 2 (png, xlsx), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | station-days whole numbers by month; per-station mean to 1 dp; grid | yes |
| Prompt | one paragraph, under 1,000 characters | 762 characters, question first | yes |
| Prompt shape / rubric | identifiable, 25+ criteria | shape 13; 23x12 grid, 12 monthly counts, 22 or 23 station means, call: well over 25 | yes |
| Em dashes | none | none found | yes |
| Reads as LLM generated | no | thread found no authoring language; leak reader's four tells were rewritten in the fix pass (not re-judged) | yes, with the caveat above |
| Goldens read as real work products | yes | not re-inspected visually by me | not independently verified |

## Gate G reconciliation
Thread: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note (## Deletion tests and Gate G) and card (gate_g now forecasting, stump_class analytical): identical on all four. The card's earlier binding_constraint label was the only mismatch and has been relabelled. The declared distractors (flood update, water quality) are not named by the thread as the surface read; the surface read the thread names as the easy route is the outlook flow taken as the published flow, which files C107 alone (1 station instead of 5), consistent with the note's rung 0. No distractor is load-bearing. Reconciled: no finding. The card's analyst_test ("the other twenty-two stations hold" on the default path, then four more fall short) is consistent with 23 stations.

## Gate H reconciliation
Thread: domain pass, layers pass, decisive_step analytical (convex-rating Jensen bias of the day's mean level, carried through the rating against the true mean). Card domain_test and layer2 (own:peaking-releases-bias-daily-mean-stage-discharge, field_method) and the design note's Three rules agree. Layer 1 (GOES UTC against local day, held messages, litres, channel rows, 2019 ratings absent from the book, Mattin renumbering) sits in the asks and does not decide the call. Reconciled.

## Stump power (Gate F)
Strong per the thread: the easy route files C107 only; skipping the 2019 rating recovery, held-message handling or Mattin pooling misses most ask cells. C124 now additionally penalises the blanket "everything downstream of a plant" shortcut, which the leak reader had flagged.

## Findings, ranked
1. (Low) The judge saw the 22-station cut; C124, the dictionary line and the rewritten documents were not judged. Per the contract no second thread is spawned; the main session's generator assertions and verify.py are the only coverage of C124.
2. (None) Card analyst_test count checked and consistent with the 23-station cut.
3. (Low) field_visits_wy2026.csv is an unnamed extra distractor; metadata names two, which meets the gate.
4. (Info) Thread's optional fix (Mattin continuity wording) is applied.

## Next action for the author
Proceed to ship; no re-judge is required (no FIX_NOW).
