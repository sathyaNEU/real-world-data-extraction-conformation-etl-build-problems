# determinism-check report, task249, 2026-10-22 (pass 2, run a6r4, target.zip 535886d8)

Written as pass 2 because determinism_check_report.md (pass 1, 2026-10-21) exists and is never overwritten.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated sonnet thread, scratch path only, executed the prompt and regulations 7.2 to 7.4 literally and reproduced the six flags (CC27-A, B, C, D, G, H), all 20 whole-number sitting counts and the critical components from the bundle. The gain splits at the 1.0 line on all eight estimator variants (flagged 1.47 to 2.39, unflagged 0.15 to 0.57). Reg 7.2's counterfactual covers the time freed by recognised items, which separates B and D. The re-sited ask A (workstation failure count, v4) reproduced exactly on all ten forms (413 total), cross-checked against the five incident-sheet layouts.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Resit sittings (2027) | 6,373 | 6,373 (via candidate_number_changes.csv) | yes |
| Scores re-keyed from bank snapshot | all | 0 mismatches over 33,562 sittings | yes |
| Latency ratio, scored / trial / same model | 0.6 / 0.7 / 0.8 | 0.55 / 0.72 / 0.78 | yes (rounded) |
| Gain per resit sitting, flagged six | 1.4 or more | 1.47 to 2.39, all variants | yes |
| Gain, other four | 0.6 or less | 0.15 to 0.57, all variants | yes |
| Excess on shown items, A/C/G/H; B/D | more than 1.0; about 0.5 | 1.44/1.78/1.15/1.16; 0.48/0.47 | yes |
| Time gain B, D; I | 0.9 or more; about 0.3 | 1.26, 1.34; 0.31 | yes |
| First-time out of time, B/D/I | 36 to 48 per cent | 40.5 / 36.2 / 47.6 | yes |
| Workstation or power failure counts A..J | 39,43,29,39,40,46,45,37,51,44 | identical (413) | yes |
| Centre link counts A..J | 64,71,53,60,73,75,71,72,84,60 | identical (683; 748 without corroboration and stop rules) | yes |

## Competing answers that survived
None. Three forks considered and closed:
- Same-model siblings as recognised: closed by the bank's item_model column, reg 3.4 and the 0.78 latency ratio. Without them C and H fall below the line.
- Time gain excluded: contradicted by 7.2's counterfactual wording, B and D then drop to 0.5. This is the intended stump, not an open fork.
- Review adds an item: a review shows only items already reached and answered wrongly, so it adds none.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 17 | yes |
| Formats | 3 or more | csv, pdf, xlsx, md, eml (5) | yes |
| Large file | 25,000 rows or more, or large database | workstation_event_log_2027.csv 59,240 rows (results r3 24,061, seat plan 18,593) | yes |
| Distractors | 2 or more in metadata, none labelled by file name | 4 named (practice_exam_orders, exam_centre_capacity, item_panel_decision_log, item_review_panel_minutes); names are neutral; judge found all unused by the solution | yes |
| Distractor weight | relevant, ruled out by a shipped fact | judge: unused by the solution; none answers a graded quantity (no gain figure in any file) | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pdf), both in golden/; no format family required | yes |
| Asks | multi-dimensional, unit and rounding stated | 10-form counts x 2 plus flagged set; "whole numbers" stated in prompt | yes |
| Prompt shape and rubric 25+ | shape 10; 25+ criteria | shape 10 named in metadata; design note estimates about 36 criteria | yes (design-side estimate, rubric is portal-generated) |
| Reads as real, not LLM generated | | judge: data_notes.md in-fiction, dates coherent, realistic layer-1 mess; golden xlsx is small (9 KB), golden-realism owns the finer read | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical, estimand_identification layer 2, decisive step "carry the time the recognised items freed to where four hours would have ended". Match. No declared distractor was named as a surface read carrying the task. The thread's two easy routes (excess on shown items gives four flags; gain over previous sitting gives nine) match the card's analyst_test exactly.

Gate H line: domain: pass, layers: pass, decisive_step: analytical. Matches the card's domain_test and the note's `## Three rules` (Decisive step, No decoy, Not semantics, Not rule application). The 7.4 counts are rule application and semantics but are asks, not the main call, so Rule 3 does not bind them.

## Stump power (Gate F)
The decisive step is the estimand's time-censoring channel (excess on shown items plus answers reached only in the freed time). The thread rates stumping likely: either easy route fails the flag set and the B and D flags, and naive WS_FAIL or NET_LOST counts miss the 7.4 answers by a lot. Caveat for the main thread: the within-candidate excess plus a reach-extension is a textbook speededness and counterfactual route; a strong solver who reads 7.2's counterfactual literally and sees 36 to 48 per cent running out of time may land it. The thread did not classify the step as the field's standard method with no judgment needed, so no landable-call note; the scored readers' result decides.

## Findings, ranked
1. None blocking.
2. Observation (judge, optional): the prompt's "its 2027 sittings" already covers all sittings, not resit only; no change needed.
3. Observation: spec-gate row for the rubric count rests on the design note, not on a generated rubric.

## Next action for the author
Proceed to stage 5 ship once the leak readers return clean; no generator change from this pass.
