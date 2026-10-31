# determinism-check report (pass 2), task250, 2026-10-31

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** APPROVE
**Stumping type:** mechanism: etl_conformance (attribution of missing observations to their source unit), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Re-judge on the pinned prompt ("how many of the extract's courier events ..."). Fresh scratch /tmp/determinism-check-task250-1793476983/, target.zip sha256 1b8dcbc7...d803b unchanged. Verdict: /tmp/determinism-check-task250-1793476983/verdict.md. Pass 1 report kept as determinism_check_report.md.

## Why
Every graded figure reproduced. All 300 door unloadings carry one hub on their sorted parcels for every idle-gap threshold from 1 to 60 minutes, so an unscanned parcel is charged to its unloading's hub. The sort plan is contradicted by 1,440 Warsaw-unloaded parcels carrying HLDZ sort events; the morning split by unloading purity. The courier-window fork from pass 1 is closed by the prompt wording.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Parcels | 91,324 | 92,161 less 837 re-sent | yes |
| Hub table | 12,600/61/0.48; 11,963/95/0.79; 16,530/222/1.34; 13,628/86/0.63; 12,178/189/1.55; 24,425/301/1.23 | identical | yes |
| Two-trailer mornings | 24; 1,440; 130; Pruszkow own 205 | identical | yes |
| Sent twice | 5,270 (13 depots) | identical; 5,118 other later records are re-attempts at 6+ minutes | yes |
| Never picked up | 2,257 (13 depots) | identical (2,046 non-marketplace + 211 marketplace) | yes |

## Competing answers that survived
None on the main call. Residual forks, all on the depot column of ask 2, none flips the call:
- Marketplace prefix collisions (435 prefixes with several orders): count-based match is the only one treating each pickup as one parcel; a set-membership match gives 0 for the marketplace part. Not stated in any document.
- PICKUP_FAILED: excluding it as a collection is the golden (step 6); including it as collected adds 468 uncollected API parcels the other way. The judge found TDS 4.4 does not define collection.
- KRK1 to KRK3 remap keyed to collection date (216 consignments differ under a sent-date reading); TDS 4.3 "from the day that depot opened" favours the collection date.
- "Same scan" rule and the hub attribution rule are not written in the TDS; the data separate both without near-ties.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10+, 3+, 25k rows | 11; 5 formats; 280,378-row parquet | yes |
| Distractors | 2+ named, no labelling name | customer_claims, hub_sorter_availability (metadata, pass 1 check); no labelling file name | yes |
| Deliverables | 1 to 3 in golden | xlsx + pptx | yes |
| Asks | multi-dimensional, unit and rounding | stated in prompt | yes |
| Rubric 25+ | 25+ | by shape (6x4 hub cells, 13x2 depot cells); rubric not generated here | yes |
| Prompt shape | identifiable | shape 10 | yes |
| Real work product | yes | no provenance leakage, coherent dates | yes |

## Gate G reconciliation
Same as pass 1: judge's mechanism and family match the design note; the sort plan is the easy route, not a declared distractor, and is not the surface read carrying the task. Judge's "Not checked: metadata.json" is covered by my pass 1 read. Match.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical; matches the card (stump_class analytical) and the note's Three rules. The decisive convention is recovered from timing, not filed (mild hidden-rule flag, answered by the note: TDS-4 files the WHAT).

## Stump power (Gate F)
Moderate to good. Plan map and per-morning split both leave Strykow unfired; Strykow carries the difficulty. Asks add layered reconstruction.

## Findings, ranked
1. Optional, depot column of ask 2 only: marketplace per-parcel pickup counting, "failed pickup is not a collection" and the collection-date remap are not stated in a shipped document. If SF rows for them are absent from the fork table, add them with a closing sentence asserted in checks.py (no prompt change needed).
2. Hidden-rule flag on the decisive convention: answered by the design note, no change.

## Next action for the author
Confirm the three ask-2 conventions have fork-table rows (add if missing), then ship.
