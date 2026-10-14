# determinism-check report, task258 (loop 1), 2026-10-14

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated sonnet thread (scratch /tmp/determinism-check-task258-loop1/, verdict.md) recomputed every load-bearing figure from the bundle. Matchday (4.6 M page loads a month, 1.40x Ledger) is forced once the counterfactual is calibrated on the eleven engagements: the load delay settles at a level (240 ms, range 232 to 247) rather than scaling, the load time scales at 0.48, and the paint cannot precede the page's own first contentful paint (the render-delay jump at E06 and E10). Charter 2.3 and 2.4 pin "moved" and the playbook's reach. Matchday stays first across the delay range 232 to 247 and ratio 0.45 to 0.50.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Delay after playbook | 240 ms | pooled 240, E range 232-247 | yes |
| Load-time ratio | 0.48 | pooled 0.479 | yes |
| Render delay E06 / E10 after | 2,321 / 2,245 ms | same | yes |
| Moved, Matchday/Ledger/Hearth/Tideline/Pantry/Trailhead | 4.6/3.3/3.2/3.1/2.9/1.8 M | 4.61/3.29/3.18/3.08/2.88/1.81 | yes |
| Slow own-image loads, Hearth | 20.4 M | 20.4 M | yes |
| Rival readings | Pantry 6.8, Ledger 7.4 / 8.4 | 6.76, 7.4-8.4 | yes |
| Egress GB | 1,208/1,056/2,102/1,971/653/667 | same | yes |
| Egress AUD | 86/75/149/140/46/47 | same, identical from rounded or unrounded GB | yes |
| Live hero images | 4,210/2,044/2,777/6,362/3,543/2,444 | same | yes |

## Competing answers that survived
No fork on the main call. Residual forks on ask 4 only:
- Live hero images without dropping legacy_id-named records: 5,027 / 3,669 / 5,184 / 6,403 / 7,921 / 4,386. By upload collection after dedup: 3,062 / 1,759 / 4,698 / 3,055 / 6,709 / 2,097 (in the thread's order Hearth, Ledger, Matchday, Pantry, Tideline, Trailhead). The golden follows the runbook (moved sections) and the charter. legacy_id is a column of the DAM export itself, but no shipped document defines it; this is the weakest committed answer (thread's note).
- Page-load rounding: figures sit 0.01 to 0.04 M from a 0.1 M boundary under pooled estimates; Ledger (3.1 to 3.5) and Hearth are least stable across the engagement range. The ranking does not move.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 16 | yes |
| Formats | 3+ | csv, md, pdf, xlsx (4) | yes |
| Large file | 25,000+ rows | rum_lcp_beacons 157,825 rows; DAM 118,869 | yes |
| Distractors in metadata.json, none labelled by file name | 2+ | crux_lcp_origins_2026-11.csv, analytics_pageviews_2026-11.csv; names do not say distractor | yes |
| Distractors unused by solution, weighable | yes | unused by the golden (thread and note agree); neither answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (md, png), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 6 properties x 4 figures; prompt states units and rounding | yes |
| Prompt shape and 25+ criteria | shape identifiable, 25+ | shape 14; design note counts 31 criteria | yes |
| Not LLM-generated; goldens real work products | yes | thread found no authoring disclosures; I did not re-sweep golden prose | yes (provisional) |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, family analytical_non_defect, surface read none, no sole data defect. Card: stump_class analytical; analyst_test names the same four routes (ratios to Ledger 7.4, no-delay preload to Ledger 8.4, level with render delay held to Pantry 6.8, level plus first-paint floor to Matchday 4.6) with the same values the thread recomputed. Design note's stump sentence agrees. The declared distractors (CrUX, analytics) were not named as the surface read. No mismatch.

## Gate H (thread)
domain: pass, layers: pass, decisive_step: analytical. Card domain_test (paint split into parts, preload/CDN connection, first-paint floor) matches the thread's reasoning, and the swap test fails to read the same. The thread's caveat: the 240 ms level and the fcp floor are an empirical calibration the solver infers from the engagement file, borderline only in that sense, not a hidden rule.

## Stump power (Gate F)
Good. The natural first move (per-part after-over-before ratios) lands on Ledger; holding the render delay lands on Pantry. Both wrong, and the engagement history separates them.

## Findings, ranked
1. Ask 4 (live hero images) is the weakest committed answer: two defensible alternative readings (no legacy_id dedup; upload-collection attribution) survive on the literal text. No effect on the call. Optional tightening in the extract log or prompt wording; no figure changes.
2. Ledger and Hearth page-load figures are near a rounding boundary under parameter uncertainty; ranking and call are stable.
3. Nothing else.

## Next action for the author
Proceed to ship; optionally add one line defining legacy_id in extract_log_2026-12-03.csv or rum_extract_field_notes.md to close the ask-4 fork, then rebuild twice and re-zip only if you do.
