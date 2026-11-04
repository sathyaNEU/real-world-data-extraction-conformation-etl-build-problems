# determinism-check report, task488 (architecture 2), 2026-11-04

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (with two design-note repairs listed under Findings; neither changes the bundle or a golden figure)
**Stumping type:** mechanism: method_or_model_selection (draw-driven plug-flow tracing validated against density samples), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated sonnet thread (scratch /tmp/determinism-check-task488-v2-1793786452, verdict.md there) recomputed the hydrant and refueller figures from the 17-file bundle. The 6,600 / 11,000 / 3,600 L section figures, the 73 hydrant uplifts and their section split, the 13 refueller uplifts, all four refueller holdings and the airline totals all reproduced. All 34 post-06:00 13 October density samples agree with the per-segment trace, and the line-fill reckoning (clear at 18:19, 64 uplifts) is contradicted by them. The thread's disposition was APPROVE.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pier B (HB-06, HB-07) | 6,600 L | 6,587 L | yes |
| Cargo apron HE-01..03 | 11,000 L | 10,996 L | yes |
| Remote stands HF-01, HF-02 | 3,600 L | 3,625 L (25 L from the 3,650 edge) | yes |
| Other sections | none | none | yes |
| Hydrant uplifts / split | 73; A33 B20 C13 E4 F3 | same | yes |
| Refueller batch at 05:30 | RF-23 3,070; RF-24 310; T-31 14,680; T-35 2,340 | 3,067; 306; 14,680; 2,343 | yes at 10 L |
| Refueller uplifts / per-row litres | 13 | 13, all rows match at 10 L | yes |
| Airline totals | 4,130 / 10,740 / 240 / 7,550 / 3,020 / 330 | same | yes |
| Per-row batch litres, about 22 partial hydrant uplifts | as filed | exact only under the steady-rate concurrent model | partial (see forks) |

## Competing answers that survived
1. **Draw ordering and the uplift count.** Under atomic draws (all at start, mid or end) the count is 72 to 74 (NG2690232 added or one dropped). Section litres do not move. **Design note: SF6 lists the alternative and states "the 73 moves by 1, 1 and 1 (asserted)"; checks.py line 141 asserts that.** It is closed by a shipped fact, not by "same call": the SCADA minute flows step by each uplift's rate (checks.py line 155 asserts the 0.3 per cent fit). Verdict: **closed, but only through a cross-file reading**. It is not filed in the prompt or QM-09. The thread's judgement is that the steady-rate model is the one the data confirm. Per-row 10 L litres on the partial rows share this dependence, and some rows sit 0.1 to 1 L from a rounding edge. This is a supplementary-ask exposure only.
2. **Tank mixing (refueller tank as one mixed body against a FIFO tank).** **Design note: SF16 does not close this.** Its listed alternative is "each delivery from the latest load" and its stated effect is "other litres". The thread's serious alternative is a FIFO tank, which leaves RF-24 and T-35 with no batch and drains only RF-23 and T-31. That changes the main call (two refuellers, Critical Component and the recommendation sentence), not just litres. The closure cited is the equipment register's Compartments column (all refueller tanks equal 1, asserted at checks.py line 180). A single-compartment tank excludes the per-compartment reading and supports a mixed body, but nothing shipped states "mixed", and QM-09 (section 2.3 defines a refueller as a vehicle tank, 3.2 quarantines any holding) does not say how a tank's contents are blended. **Status: open on the main call at the table level, closed only by physics (a tank is not a pipe).** The thread treated mixed as the only defensible expert convention.
3. Line-fill reckoning, N-7 always on T-31, and counting the voided ticket (74) did not survive.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 17 | yes |
| Formats | 3 or more | CSV, XLSX, PDF | yes |
| Large file | 25,000 rows or more | hydrant SCADA CSV, 44,070 rows | yes |
| Distractors | 2 or more, named in metadata, none labelled in a file name | pit_valve_inspections_2026-q3.xlsx, stock_reconciliation_2026-09.pdf; both named in metadata.json; file names do not label them | yes |
| Distractor role | unused, relevant, ruled out by a shipped fact, does not answer a graded quantity | thread found both relevant but unused; neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden, no format family required | 2 (CSV and PDF with a schematic), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | per-uplift rows, section, refueller and airline cuts; the prompt gives the 100 L and 10 L rounding and 15 C | yes |
| Prompt shape / rubric 25 or more | shape 07; 25 or more criteria | shape 07 named in metadata; 86 uplift rows plus 7 sections, 8 refuellers and 6 airlines give well over 25 gradable items (rubric itself not generated here, not checked) | yes (inferred) |
| Not LLM generated / golden realism | | thread found no authoring text; golden is a recall return CSV and a plan PDF | yes |

## Gate G reconciliation
| Field | Thread | Card / design note | Match |
|---|---|---|---|
| mechanism | method_or_model_selection (plug-flow tracing validated against densities) | driver: substance displaced through a branched always-full network by downstream draws; stump sentence: per-segment front against the line-fill reckoning | yes |
| stumping_family | analytical_non_defect | stump_class: analytical; "No decoy" line present | yes |
| surface_read_dependency | no | the declared distractors are the pit valve inspections and a stock reconciliation, neither named as the surface read | yes |
| sole_data_defect | no | design note: nothing planted | yes |

The thread names the line-fill reckoning as the tempting wrong route, as the design note does. The reckoning rests on the operator's routine product-change checks (true where taken) and is not a declared distractor, so the distractor is not too load-bearing. The thread notes the shift log's line-fill framing is not an official wrong-method artifact.

## Gate H reconciliation
Thread: domain pass, layers pass, decisive_step analytical. Design note and card: the domain test (position of the batch per segment) matches, the analyst test (strong analyst files a clear hydrant and 64 uplifts) matches, and `stump_class` is analytical. "Not semantics" and "Not rule application" hold: QM-09 files what to drain, not how the position is found. The three-rules block in the note lists a Task type, Swap, Layer 1 and Layer 2 line, which the thread matches. **No mismatch.**

## Stump power (Gate F)
Heavy work: 243 hydrant tickets, 70 refueller tickets, flushes, a trailer swap, a rack line fill, a tank-to-tank transfer. The easy route (line-fill reckoning, no section to drain, 64 uplifts) is wrong on the density evidence. The thread rates it not too easy. Plug-flow displacement tracing is a recognised method in a pipeline engineer's field, but the golden is reached only by modelling each segment's draws; the thread did not describe a landable shortcut. Risk runs the other way: strict 10 L grading of the partial rows may punish correct work that differs only in numeric method.

## Findings, ranked
1. **SF16 understates the tank-mixing fork.** The table says the alternative gives "other litres". The FIFO-tank reading gives a different drain list (RF-24 and T-35 off the list). Repair: add a FIFO-tank row to SF16 with its true call effect, name the closing shipped fact, and add an assertion in checks.py (currently only the compartment count is asserted). If the author wants the fork closed in the files, add one shipped sentence that a refueller tank commingles its loads (for example in QM-09 or the equipment register notes), which files the WHAT and not the HOW. The thread's optional Option 3 is the same step.
2. **SF6 closes the count only through the SCADA minute flows.** Acceptable as written, since the design note asserts it. If the bundle is left as is, the per-row litres on the 22 partial rows are the main supplementary-ask exposure. Option: coarsen those rows or accept it.
3. Several rows sit within 0.1 to 1 L of a 10 L rounding edge (CB418319, CB418378, CB418369). Residual and supplementary only.

## Next action for the author
Edit SF16 in DESIGN_NOTE.md to carry the FIFO-tank alternative with its real call effect (RF-24 and T-35 dropped) and assert the mixed-body reading in checks.py; decide whether to file one commingling sentence in the shipped files. No re-judge is needed unless the bundle changes.
