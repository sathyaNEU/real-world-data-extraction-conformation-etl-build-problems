# determinism-check report, task250, 2026-10-31

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** APPROVE (optional prompt pin for the courier-event window, see Findings)
**Stumping type:** mechanism: decomposition_attribution (etl_conformance asks), stumping_family: analytical_non_defect, surface_read_dependency: no (borderline), sole_data_defect: no

Thread verdict: /tmp/determinism-check-task250-1793475852/verdict.md. target.zip sha256 1b8dcbc7...d803b (architecture 3).

## Why
Every graded figure reproduced from the bundle alone. The alert set Sosnowiec, Strykow, Pruszkow follows once an unscanned parcel is charged to the hub of the unloading it came off: all 300 door unloadings carry one hub on their sorted parcels, and idle thresholds of 1 to 29 minutes give the same split. The competing routes (sort-plan hub, depot-morning split, mixed mornings dropped) are each ruled out by a shipped fact.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| October parcels | 91,324 | 92,161 rows less 837 re-sent = 91,324 (depot_scan_events) | yes |
| Hub table (parcels/missed/rate) | HPOZ 12,600/61/0.48; HWRO 11,963/95/0.79; HKTW 16,530/222/1.34; HKRK 13,628/86/0.63; HLDZ 12,178/189/1.55; HWAW 24,425/301/1.23 | identical | yes |
| Two-trailer mornings | 24; 1,440 parcels, 130 missed; HWAW own 205 | identical | yes |
| Sent twice per depot | 5,270 total (581, 125, 600, 272, 324, 375, 97, 200, 127, 599, 292, 942, 736) | identical | yes |
| Never picked up per depot | 106, 257, 162, 139, 110, 195, 43, 86, 170, 189, 309, 145, 346 | identical (needs de-duplicated pickups; else 15 low) | yes |

## Competing answers that survived
- Courier-event window (ask 2, sent-twice column only): prompt gives none. Golden counts every record in the extract (30 Sep to 3 Nov). Restricting to 1 to 31 Oct gives 5,179 and moves KRK1 92, LDZ1 579, POZ1 569, WAW1 926, WAW2 727, WRO1 595. Literal reading (TDS-4 3.1 and 5.1, the platform as extracted) matches the golden. Does not touch the main call. Not in the design note's fork table (SF17 covers duplicates only, not the window).
- Hub-routes (plan hub, depot-morning split, exclusion): do not survive.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10+, 3+, 25k rows | 11 files; 5 formats (csv, eml, parquet, pdf, xlsx; the thread said 6, I count 5); 280,378-row parquet | yes |
| Distractors | 2+ named in metadata, no file name labels | customer_claims, hub_sorter_availability; neither has a labelling name; unused by solution, no bearing on figures | yes |
| Deliverables | 1 to 3, all in golden | xlsx + pptx, both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | hub table, 13-depot pair, chart; prompt states per cent, two decimals, whole counts | yes |
| Rubric 25+ criteria | 25+ | not generated here; per-hub (6x4) and per-depot (13x2) cells exceed 25 | yes (by shape) |
| Prompt shape | identifiable | shape 10 in metadata | yes |
| Reads as real work product / not LLM | yes | thread found system-extract mess, coherent timeline, no provenance leakage | yes |

## Gate G reconciliation
Thread: mechanism decomposition_attribution, family analytical_non_defect, surface_read_dependency no (borderline), sole_data_defect no. Design note: stump is attribution of unscanned parcels to the unloading's hub; the sort plan is declared an ordinary route of record, not a decoy. The sort plan is not a declared distractor in metadata (distractors are claims and sorter availability), and the thread names it as the easy route, not as carrying the task: it is a Layer 1 artifact the unloadings refute. Match. No distractor is too load-bearing; Gate G is satisfied since the plan is correct as a plan and states no rate.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical. Matches the card (stump_class analytical) and the note's Three rules (No decoy, Not semantics, Not rule application). Mild flag from the thread: the convention is recovered from timing structure, not filed, so a strict reader could call it a hidden rule. The note's answer is that TDS-4 files the WHAT and the data's unloadings force the HOW.

## Stump power (Gate F)
Moderate. The sort plan, depot-morning split and exclusion routes each end on a wrong alert set (Strykow under the line); only the unloading reconstruction from door timestamps lands it. Discoverable from the data (register's manual sort hall is a faint pointer). The asks add layered reconstruction (clock by handheld model, piece labels, de-duplicated pickups, replaced depot).

## Findings, ranked
1. Courier-event window not filed in the prompt or the fork table (ask 2, sent-twice column, six depots move). Fix, either: add a fork-table row (window = every record in the extract, TDS-4 3.1 and 5.1) asserted in checks.py, or add a prompt clause; the prompt clause changes what solvers see and needs a rerun. Not blocking.
2. Mild hidden-rule flag on the decisive convention, answered by the design note; no change needed.
3. Format count in the thread's hygiene section is 6, actual 5; passes either way.

## Next action for the author
Add the courier-window row to the design note's fork table and assert it in checks.py (no prompt change); then proceed to ship.
