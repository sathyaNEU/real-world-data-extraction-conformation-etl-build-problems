# determinism-check report (pass 2), task469, 2026-10-17

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judge thread: one general-purpose sonnet medium thread on a fresh unzip at /tmp/determinism-check-task469-277391/target/; verdict at /tmp/determinism-check-task469-277391/verdict.md. (The spawn was done by the main session; I wrote the brief, then reconciled after the verdict returned.)

## Why
The main call is forced by shipped text: SFG-3 2.4 and 3.1 to 3.3 file the need definition, the 20 per cent standard, the 15 Jun to 15 Sep window and the five-minute steps. Every decisive step is far from the line (7.6 vs 26.9, 6.3 vs 26.3, 4.7 vs 30.6 per cent), and the product-limit estimate and the conditional share give identical decisions. Asks 1 to 7 are forced. Ask 8 reproduces exactly once double-filed rotations are removed, but the shipped text never states that rule (see forks).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Turns, six relationships | 2731/1114/2398/1023/930/1016 | identical | yes |
| Share over filing, Norvale-Pellmont 35 | 27 | 26.9 | yes |
| Norvale-Grayling 40 | 6 | 6.3 | yes |
| Norvale-Sable 30 | 7 | 7.0 | yes |
| Tellura-Pellmont 40 | 26 | 26.3 | yes |
| Tellura-Sable 30 | 31 | 30.6 | yes |
| Grayling 35 | 1 | 0.7 | yes |
| Shortest accepted | 40/40/30/45/35/30 | 40/40/30/45/35/30 | yes |
| Ask 8 turns/shorter | 213/42, 84/21, 189/42, 105/28, 91/28, 77/21 | same, after removing double-filed rotations | yes, by inference only |

## Competing answers that survived
- Ask 8 population: the literal count of every filed turn gives 290/63, 133/56, 259/63, 231/119, 168/42, 161/42. No shipped sentence says a rotation filed under two brands counts once or which twin is operating. The golden follows only by inference: 141 new-number flights duplicate a partner's s26-carried rotation, and counting them needs 19, 17 and 11 aircraft lines against 13, 12 and 7 in kdy_regional_fleet_plan_s27.csv (12, 11, 6 after removal). The route is derivable from shipped files, not filed. Confined to ask 8; the judge rates the risk low to moderate.
- Minor, no decision moves: shortest acceptable for an accepted filing is a five-minute step by SFG-3 3.3 reading; chart step (5 vs 1 minute) not pinned; 202 turns with both held and not-ready minutes leave the order unstated.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 16 | yes |
| Formats | 3+ | 4 (csv, xlsx, pdf, ssim) | yes |
| Large file | 25,000+ rows | AODB 28,392 rows | yes |
| Distractors | 2+ in metadata.json, no file name labels | punctuality workbook, staffing csv; unused by the solution per judge | yes |
| Distractor weighs | arithmetically reproduces a graded quantity, ruled out by shipped fact | not tested separately; the judge found neither ranks turn need | partial, see findings |
| Deliverables | 1 to 3 | 1 xlsx, present in golden (4 sheets, 1 chart) | yes |
| Asks | multi-dimensional, unit and rounding stated | whole minutes and whole numbers stated | yes |
| Prompt shape and rubric 25+ | shape 14 identifiable; criteria | shape named in metadata; 6 relationships x several figures plus chart; rubric count not generated here | likely yes |
| Reads as real | no LLM feel | judge saw none; mixed system layouts read as real exports | yes |

## Gate G reconciliation
Judge: mechanism statistical_rigor, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: analytical censored-need estimation; analyst test sends back three only with the censoring-aware estimate, observed overruns accept all six, stand time sends all six back. Matches. Declared distractors (punctuality, staffing) were not named as carrying the task. Gate G classification: pass, no shipped artifact ranks candidates on the decision question wrongly; no decoy.

Gate H line: domain: pass, layers: pass, decisive_step: analytical (censored estimate of turnaround need against a coordinator percentile standard; Layer 1 is UTC/local, hyphen, sub-code, delay-field and tow mess). Matches the note's `## Three rules`.

## Stump power (Gate F)
Strong. Two natural routes file wrong answers (stand time as need: all six sent back; coded overrun over all turns: all six accepted, at most 19 per cent). Only the censored estimate sends back three.

## Findings, ranked
1. Ask 8 double-filed-rotation population is inferred, not filed (optional fix; ask-only, not the main call).
2. Minor unpinned conventions: chart step, five-minute step wording for accepted filings, order of held vs not-ready minutes.
3. I did not independently confirm that the distractors are arithmetically a wrong-basis answer; the judge only found them unused.

## Next action for the author
Optional: add one prompt clause (or rely on the fleet plan) fixing that a rotation filed under two brands counts once under the flights the 2026 season schedule already carried. This changes what solvers see, so it needs a rebuild and re-judge; otherwise proceed to ship.
