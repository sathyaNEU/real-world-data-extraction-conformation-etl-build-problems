# determinism-check report, task489, 2026-11-04 (pass 2)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection (etl_conformance mess underneath), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

The thread kept the order: derivation.md was written from target/ alone before graded_blocks.md was opened. This is the architecture's one valid re-judge. Thread files: /tmp/determinism-check-task489-r1793813844/verdict.md and derivation.md. The pass-1 report is untouched and was not shown to the thread.

## Why
Every deciding fact is in the bundle: the plan's 0.5 t line (s.3), MRS-03 s.3.2 and s.4.2 (production-day window; counted cycles where counted, otherwise cycles x the maker's rated gas), the three makers' logic sheets (open at the high setting, shut at the low) and the PCX-300 spec (liquid reaches surface ahead of the plunger). Replaying the controller logic on each well's slug against its own band gives 8 pads. The thread's derivation matched the submission on every graded figure before it saw the submission.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Five dump counters, unwrapped at 65,536 (scada_dump_counters_2026.csv) | 21,178 / 19,584 / 51,914 / 58,697 / 47,178 | same | yes |
| 51 per-controller kg | as submitted | identical | yes |
| 26 pad tonnes (8 in: Kakwa 3-9 0.95, 11-22 0.86, 14-16 0.75, 6-27 0.74, Elmworth 10-11 0.71, Kakwa 16-23 0.70, Elmworth 7-2 0.64, Kakwa 1-14 0.62) | as submitted | identical | yes |
| 25 no-arrival counts (PCX-300 counters, production-day window; 17,211 total) | as submitted | identical | yes |
| Sales PC kg: Aldous E 518 / K 259, Corrigan E 379 / K 434 | as submitted | identical | yes |

## Competing answers that survived
None on the main call or any ask. Forks tested and closed:
- Liquid over band for every uncounted separator: 11 pads (adds Kakwa 8-10 704 kg, Elmworth 5-3 638, Elmworth 12-15 571). The data separate it from the golden: slug/band is bimodal (12 separators at 2.0 to 3.5 x band, 13 at 0.02 to 0.1), and a valve held open to the low setting empties a band once per slug.
- One dump per arrival: 11 pads (drops those three, adds Elmworth 4-27 626, Elmworth 9-34 620, Kakwa 13-22 637). Needs 20 to 90 arrivals per dump on the small-slug wells.
- Liquid spread through the afterflow (Reading 2): reproduces the liquid-over-band set and is ruled out by the PCX-300 spec's own words ("brings that liquid to surface ahead of it as it arrives").
- Survey rate x 8,760 h (Reading 4): ruled out by MRS-03 s.4.2 ("its maker's rated supply gas per dump cycle"); the design note's ladder files it at 18 pads.
- Counter rollover (Reading 5): 65,535 against 65,536 moves a count by 1 (0.01 kg); the PCX-20506 step of -8,423 is a well move, not a rollover.
- Two-phase liquid (Reading 6): condensate plus water; condensate alone fits the counters at 0.62 to 0.78, total liquid at 0.98 to 1.01.
- Cycles without an arrival (Reading 7): counters 17,211 against the host's logged NO ARRIVAL rows 11,549. The host log drops rows, and the PCX-300 spec's counter definitions rule it out. Calendar 2026 against production day moves a well by 0 to 3 cycles; MRS-03 s.3.2 files production days.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 18 at the archive root | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, docx) | yes |
| Large file | 25,000 rows or more | plunger_cycles_2026.csv, 240,864 rows | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | 4 named (ogi_leak_survey, tank_vent_measurements, volumetric_adjustments, allocation_runs); no file name says distractor | yes |
| Distractor behaviour | unused by the solution, relevant enough to weigh; one that answers a graded quantity is ruled out by a shipped fact | none answers a graded quantity; leak survey and tank vents are other sources (MRS-05, MRS-07), the journal and run log carry gas re-runs only | yes |
| Deliverables | 1 to 3, all in the golden, no format family required | 2 (xlsx, pptx), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 4 asks (51 controllers, 26 pads, 25 wells, 4 maker-by-area cells); kg to the nearest kg, tonnes to 2 dp, counts | yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | shape "other", declared; criteria from 26 pads, 51 controllers, 25 wells and 4 maker cells run well past 25 | yes |
| Reads as human and real work product | nothing LLM-looking | the thread saw no authoring language; real operational mess; I did not re-run the golden-realism read | yes (as far as this pass checks it) |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no.
Card: gate_g etl_conformance, stump_class analytical, layer2_family field_method, stump "separator dumps under plunger slugs against each level controller's band".
- The stump is the same on both sides: the liquid-over-band estimate that the five counters confirm, against the slug-versus-band count. The thread names the default path the card names, and finds the same 11-pad list with the same three pads added.
- The labels differ only in mechanism. The card files the build under etl_conformance, as the objective requires; the thread classes the decisive step as method selection with conformance mess underneath. Both are non-banned mechanisms and the stumping family agrees. Not a send-back finding.
- The declared distractors (OGI leak survey, tank vents, journal, run log) are not the surface read carrying the task. The wrong reads are the liquid-over-band and one-dump-per-arrival estimators, neither a distractor. `surface_read_dependency` is no.
- The design note's ladder (11, 11, 18, 14 and 8 pads) matches the thread's alternatives exactly.

## Gate H (three rules)
domain: pass, layers: pass, decisive_step: analytical.
The thread, the design note's `## Three rules` and the card's `analyst_test` and `domain_test` agree. The deciding quantity is each controller's dump count, which an emissions inventory estimates; Layer 1 is the moved controllers with stale labels, the wrapping counters, the re-sends, the lossy host log and the renumbered tags. A strong analyst who cleaned everything and read every rule would still file the 11-pad liquid-over-band list.
One point for the main thread to weigh. The note's "Not rule application" line says no sentence compares a well's arrivals with its liquid, so the ruling-out is silent. The thread says the makers' sheets and the PCX-300 spec rule out all but the replay, and it derived the replay from them without help. Both can hold: the sheets file device behaviour, not a counting procedure.

## Stump power (Gate F)
The thread rates it strong. The five counters invite liquid over band (11 pads), and the plunger log invites one dump per arrival (a different 11). Only the slug-against-band replay gives 8. The margins are large: Kakwa 1-14 sits 122 kg over the line and Elmworth 14-24 88 kg under it. Per the design note, each flipped pad is 1.5 times or more higher under its wrong route than under the golden. The decisive step is analysis the data settle, not a hidden rule. No landable-by-textbook-method concern is raised: the field's standard frequency estimate (liquid over band) is the wrong route here, and the thread reached the golden by replaying device logic against the data, not by applying a standard method.

## Residual risks recorded from the thread
1. **The five counters fit liquid over band to within about 1.7 percent per separator.** Elmworth 7-2's pad figure (643.90 kg) is 1.1 kg under the 0.645 t rounding line at two decimals. Kakwa 16-23 (703.88 kg) is 1.1 kg under 0.705 t.
   - Under the literal formula (liquid over band for each uncounted flowing separator) every figure reproduces to the digit.
   - A solver who scaled the uncounted separators to the counters' fit could move per-controller kg on the flowing separators and the 2 dp pad figures for Elmworth 7-2 and Kakwa 16-23. For example, +1.7 percent on LC-070201 (583 kg) adds about 10 kg and takes the pad to 0.65 t.
   - No file licenses that scaling. MRS-03 s.4.2 files counted cycles where counted and the maker's rated gas per cycle otherwise, and the counters cover five separators only.
   - It does not move the 8-pad call, the 51 controller figures, the plunger-well counts or the maker totals under any filed reading.
   - It is a rounding-edge risk on a few pad-tonne and flowing-controller figures, accepted as a risk, not a fork.
   - Correction to the thread: Kakwa 8-35 (3.86 kg) sits 0.36 kg from the 3.5 kg line and about 0.64 kg from 4.5 kg at nearest-kg precision, not 1.1 kg from 5. A 1.7 percent shift moves it by about 0.07 kg, so it does not change.
2. **No file gives a drain rate or a slug arrival speed.** The thread finds the set holds while a slug arrives faster than its valve drains. The design note's SF17 and sweep assert the same condition.
   - The sweep covers drain 1.5 to 7 m3/h (1 in body) and 3 to 25 (2 in), slug speed 0.6 to 1.6 of the plunger's average, afterflow liquid 0 to 15 percent and effective band 0.9 to 1.1. All 24 corners file the 8 pads, and every big-slug controller opens once per arrival.
   - The thread's own check agrees: band volume +-30 percent leaves the set unchanged, since the smallest slug is 2.0 bands.
   - A valve that drains faster than a slug arrives is outside the sweep and outside anything a file or the physics licenses.
   - It moves no graded figure under any reading the files license.

## Findings, ranked
1. No blocking finding. Verdict DETERMINISTIC, disposition APPROVE.
2. Rounding-edge exposure on Elmworth 7-2 (0.64 t) and Kakwa 16-23 (0.70 t), each 1.1 kg from a two-decimal line, and on flowing-separator controller kg, if a solver scales to the counters. Closed by the literal formula; recorded, not a fork.
3. The note's "ruling-out is silent" wording and the thread's "data sheets rule out" are two accounts of one mechanism. Optional wording tidy-up in the note.
4. The cross-batch check against delivered tasks was not possible from the thread's allowed paths. The card's differentiation section lists five neighbours.

## Next action for the author
Proceed to stage 5: no repair is needed. Optionally state in the design note that the flowing separators' figures are the literal liquid over band, not counter-scaled, so the rounding-edge exposure on Elmworth 7-2 and Kakwa 16-23 is on file.
