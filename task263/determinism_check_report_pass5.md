# determinism-check report, task263 (pass 5), 2026-11-02

Target: target.zip md5 7a18885f5f63334818699b3ce753f30a. One isolated thread (brief at /tmp/determinism-check-task263-p5/judge_brief.md; the coordinator removed the brief's item 4, the description of the operating-report change, before the thread ran, so it read the files cold). Thread verdict: /tmp/determinism-check-task263-p5/verdict.md.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (thread's disposition; one optional hardening, see Findings)
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Every graded figure reproduced from the shipped files: 23 of 53 wells, all 20 grants, 16 systems reached, Nordvold first unreached, USD 451,200 left, and the 16 county-quarter water cells. Section 6.3 ("a well's own water is the water the well itself pumps") and 6.4 pin the estimand. Entry-point flow equals the summed rated capacity of the wells in service (ratio 0.95 to 1.06) and every entry point's well system has full column rank, so the unmixing has one answer. The 23-well set and the 16-system call do not move under any reasonable cleaning choice. Only the naive entry-point-average route gives a different call.

The pass-4 fork (netting the second well in all 12 months vs only lead months) is closed by the files: readings (b) and (c) differ in one cell, Granlund Q1, by 0.030 MG, and both round to 291.6.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Samples (2024-25, RT/CO, PFOA/PFOS) | 302 usable (305 less 3 with sources not recorded) | 305, 3 unrecorded, 302 | yes |
| Wells over 4.0 ng/L | 23 of 53 | 23 (over-line wells 5.05 or more, rest 2.39 or less) | yes |
| 16 funded grants | 1,728,000; 6,000,000 (cap, from 6,220,800); 3,456,000; 1,382,400; 2,419,200; 2,592,000; 2,764,800; 1,900,800; 3,283,200; 1,555,200; 1,209,600; 3,801,600; 1,036,800; 864,000; 1,036,800; 518,400 | identical | yes |
| Funded total / left | 35,548,800 / 451,200 | same | yes |
| Nordvold / Glomstad / Ekholm / Opsahl | 691,200 / 691,200 / 518,400 / 1,209,600 | same | yes |
| Water Q1-Q4 Granlund | 291.6, 341.2, 387.1, 307.1 | 291.576 (b) / 291.606 (c), 341.2, 387.1, 307.1 | yes |
| Water Engvall | 283.8, 329.6, 381.7, 296.6 | same | yes |
| Water Hedstrom | 196.4, 229.3, 263.7, 208.2 | same (262.9 Q3 if emergency well excluded) | yes, one live alternative |
| Water Sandholm | 153.4, 179.7, 207.0, 163.8 | same | yes |

Sensitivities that each leave 23 wells, 16 systems, 451,200: FD and FRB samples included; RT only; 2026 samples included; lowest revision; non-detects at zero or at the reporting limit; equal-share mixing.

## Competing answers that survived
Water ask, readings tried (million gallons, Q1/Q2/Q3/Q4):
- (a) each line as written, each meter once: Granlund 326.5/415.4/426.4/383.8; Engvall 314.4/364.5/416.3/330.0; Hedstrom 215.6/247.9/282.5/227.2; Sandholm 167.4/194.8/228.1/180.0. Double counting, 14 to 77 MG too high in every cell. Ruled out by the pump ceiling (four lines exceed capacity times days in service, up to 6.9x; "constant speed" per the pump column; every other well at 0.88 of capacity or below).
- (b) net the second well in every month it runs: the golden.
- (c) net only in beyond-capacity months: identical to (b) except Granlund Q1 291.606 (Lindvik Lake Well 2's one-day sampler visit, 30,089 gal); rounds to 291.6. Not a fork.
- (d) take the piped wells' own meters off, keep the lines: identical to (b) in all 16 cells. (d2) drop the wellhouse lines, keep the piped meters: undercounts 15 to 82 MG a cell.
- Netting any other well of the host system leaves 0 of 4 (or 0 of 6) months feasible; the piped-in well is the only feasible one in all four systems.
- (e) each meter once: Skogen's two wells share a header meter with the volume repeated on both rows; counting both inflates Hedstrom to 250.9/290.4/332.6/265.8. Wrong by the filed rule.
- Emergency well (Kesselring Well 3, 3 days, 0.799 MG in Q3): included by the golden under the prompt's literal "wells" (the chart ask says "active", this ask does not). Excluding it gives Hedstrom Q3 262.9 not 263.7. The one cell of 16 with a live alternative reading.
- Emergency interconnection (Ackerholt Creek from Mossham Creek, 2.666 MG in September): not a well, excluded; including it gives Granlund Q3 389.8.
- Quarter boundaries: rows are calendar report months, no day-level reads, no ambiguity. No cell within 0.01 of a rounding edge (nearest Granlund Q4 307.100).
- Fjelstad Well 2 June meter swap (M-100525 removed 2025-06-12): meter_end minus meter_start is negative; volume_gal is used. County equals Table 6-1's for all 20 systems. Wholesale sales not deducted (water pumped).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 12 | yes |
| Formats | 3 or more | csv (9), pdf (2), xlsx (1) | yes |
| Large file | 25,000 rows or more | pfas_entry_point_results_2024-2026.csv, 36,414 rows | yes |
| Distractors | 2 or more named in metadata.json, none labelled by file name | 4 named (national survey 2023, private well results, system register, wholesale connections); file names carry no label | yes |
| Distractor quality | unused, weighable, ruled out by a shipped fact | survey is in micrograms per litre with no sources in service; none answers a graded quantity; thread found no contamination | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, png), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | grant per system with reach; 4 counties by 4 quarters; "dollars to the dollar, water in million gallons to one decimal" | yes |
| Prompt shape / 25 criteria | identifiable, 25 or more | shape identifiable (every system, well and county-quarter graded); rubric count is generated downstream and not checked here | not verified |
| LLM-read / realism | none | thread found no authoring language, dates coherent; golden realism not re-read by me | yes (thread) |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card/design note (read after the thread returned): task type emissions inventory serving Descriptive & Distribution; layer 2 is the decomposition and attribution family (mass-balance unmixing of entry-point blends); declared stump is the single-well averaging route. Match on mechanism and family. The declared distractors (national survey, private wells, system register, wholesale connections) were not named as carrying the task. Minor difference in the easy route's size: the thread's entry-point-average route gives 49 wells, 6 systems, 4,694,400 left; the design note's default path (the average of the samples each well ran in) gives 7 systems, Nesvold, USD 672,000 left, and the submission also files 8 and 11. Same family, same direction, both far from 16; no mismatch in kind.

Gate H line (thread): domain pass, layers pass, decisive_step analytical. Matches the note's Domain test, Layer 1/2 and Decisive step (inverting the mixtures). The thread did not class the step analytical because it is a standard method; it found the easy route lands a different call on clean data.

## Stump power (Gate F)
Strong per the thread. A capable analyst who cleans and reads the rules still averages the samples over the wells at each entry point (6 to 11 systems against the golden 16). The water ask adds an independent trap: as-written line sums are 14 to 77 MG high per cell, and only the capacity ceiling shows the piping. The unmixing is a textbook mass balance, so a strong solver may land it (stumping 1.3); the main thread weighs that against the note's ladder.

## Findings, ranked
1. Hedstrom Q3 (one cell of 16): the emergency well is included on the prompt's literal "wells" (263.7); excluding it gives 262.9. The literal reading of the prompt supports the golden, so this is a residual, not a fork. Optional close: say "all wells, active or emergency" in the ask.
2. No shipped sentence states that a second well discharges through a host's wellhouse. The meter register lists each wellhouse line under its own well only; the netting rests on a pump-capacity inference that the thread found has exactly one feasible answer in all four systems. Optional close: a location note on the four wellhouse lines ("also receives discharge of Well 2"); it changes no number.
3. Reading (c) vs (b) differ by 0.030 MG in Granlund Q1; both round to 291.6.

## Next action for the author
None required; the build is clear to continue to the remaining stage-4 checks. If the author wants the water ask closed by words, make the two optional edits in Findings 1 and 2 (no number moves); that would need the usual gates re-run and is the author's call.
