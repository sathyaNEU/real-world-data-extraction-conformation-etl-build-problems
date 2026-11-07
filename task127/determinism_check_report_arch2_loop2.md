# determinism-check report, task127, 2026-10-16 (cut-1 pass, loop 2)

This records the judge thread run on cut 1 of the loop-1 hardening reship (notes sentence defining the Hospital discharge route, merger-closed practices, three-rules block). The pack was re-cut afterwards (waits redrawn right-skewed; total bed-days 7,160 became 6,723). This verdict does NOT cover the re-cut; a fresh pass on the re-cut is separate (brief at /tmp/determinism-check-task127-loop2b/judge_brief.md).

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (on cut 1)
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Allocation note SF-2026-14 files the estimand (pathway 1, new package, Marchshire-ICB practice, ready date 1 Dec 2025 to 28 Feb 2026; value = nights a package would have shortened the stay; cap at covered count; 1,200 split to maximise bed-days). The ICES notes plus the data (0 of 789 delivered patients left before delivery) force a counterfactual stay from max(ready date, delivery) to discharge. Greedy fill follows. Values were well separated (6.65 > 6.24 > 5.26 > 4.36 > 3.60) and the 1,200 cap binds only at Cleeve Park / Ashby Vale, so 508/350/120/222/0 was forced. Soft spots: the PDF does not mention equipment (inference from ICES notes and data; the naive "nights after ready" reading is a different estimand, not a defensible reading of "shortened their stay"); ward-at-midnight attribution is implied by the ward-stays file.

## Recomputation ledger (cut 1 values; superseded for values by the re-cut)
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Covered patients RM/WB/HI/CP/AV | 508/350/120/285/361 | same (1,624) | yes |
| Nights per patient | 6.65/6.24/5.26/4.36/3.60 | 6.6476/6.2400/5.2583/4.3614/3.5983 | yes |
| Naive nights after ready AV/CP | 10.30/9.67 | 10.30/9.67 | yes |
| Bed-days by hospital, total | 3,377/2,184/631/968/0, 7,160 | same, unrounded 7,160.23 | yes |
| Spells leaving on delivery day AV | 129 of 361 | 129 | yes |
| Brokerage <=7 days (3 districts x 3 months) | 169/189/146; 34/35/39; 92/96/77 | same | yes |
| Chart cells, total 23,541 | all 15 cells | all match | yes |

## Competing answers that survived
None that change an answer. Forks tested and closed or immaterial: dedup rule (cohort identical under first/latest/all), closed practices (no covered patient affected), Started-only brokerage counts (smaller; "took" read as having a start date, mild wording risk), chart site by discharge site vs ward at midnight (moves 638 nights; ward at midnight is what occupied bed-days at the hospital means), month by evening date (stated in the extract notes).

## Spec gates (checked by me on the bundle/metadata, not exhaustively re-run on the re-cut)
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats | >=10 / >=3 | 16 / 4 (csv, txt, xlsx, pdf) | yes |
| Large file | >=25,000 rows | 138,606 (ward stays), 65,5xx (discharges) | yes |
| Distractors | >=2 named in metadata, none in a file name | 3 named (weekly return, bed census, reablement outcomes); file names do not label them | yes |
| Distractor relevance | unused, weighs, ruled out by shipped fact | weekly return reproduces the naive nights after ready (AV 10.30, CP 9.67) and is ruled out by the equipment dependency in the ICES notes/data | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, svg), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 9-cell district x month grid; 15-cell hospital x month chart; whole numbers stated | yes |
| Rubric >=25 criteria | 25 | not generated at my stage; asks give 5+5+1+1+9+15x2 gradable figures, well above 25 | yes (inferred) |
| LLM-read / golden realism | none | judge found system-extract mess, no authoring disclosure | yes |

## Gate G reconciliation
Thread: mechanism decomposition_attribution, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: decisive step is valuing a package at the counterfactual saving (later of ready date and equipment delivery to discharge), an analytical decomposition of concurrent dependencies; sole-defect none. Match. Declared distractor (weekly return) is the surface read that produces the wrong answer, as a trap path, not as carrying the task: the difficulty survives deleting it because the naive nights after ready come directly from the discharges file. No finding. Note: the card (stump_class/analyst_test/domain_test) was not located by me in a single card file; the design note's Three rules section carries the analyst test, domain test and decisive step and agrees.

## Gate H
domain: pass, layers: pass, decisive_step: analytical. Matches the design note's Three rules (Domain test, Layer 1, Layer 2, Analyst test, Decisive step). Soft spot: the equipment link is a join plus domain reasoning; the note says "would have shortened their stay" so it is an estimand, not a withheld rule.

## Stump power (Gate F)
Moderate to good. Naive route puts AV first (361) and CP second, wrong ranking and a much larger total; asks add independent failure chances (spot-invoice care starts, ward-at-midnight nights).

## Findings, ranked
1. Cut 1 verdict stands only for cut 1. The re-cut changed values, total bed-days (6,723) and both asks' cells, so every figure in the ledger above must be re-verified by the pass on the re-cut. 
2. Soft spot: PDF silent on equipment; closed by ICES notes sentence plus data. Leave as is (pinning discharge-before-delivery would disarm the trap).
3. Mild wording risk: "took" for brokerage referrals.

## Next action for the author
Have the orchestrator spawn the re-cut judge from /tmp/determinism-check-task127-loop2b/judge_brief.md and re-invoke determinism-judge with its verdict.md; do not ship on the cut-1 verdict.
