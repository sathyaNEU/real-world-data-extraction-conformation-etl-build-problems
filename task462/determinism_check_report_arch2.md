# determinism-check report, task462 (architecture 2), 2026-11-04

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (one optional tidy, see Findings)
**Stumping type:** mechanism: estimand_selection (base surface for stockpile volume), stumping_family: method_or_model_selection, surface_read_dependency: no, sole_data_defect: no

Judge verdict file: /tmp/determinism-check-task462-v2-1793784528/verdict.md (one thread, sonnet, medium; brief at judge_brief.md in the same folder; target.zip sha256 07da6cdd...1169e3).

## Why
Every committed answer (six pile areas, 150,000 t, 62 days, the call, receipts by coal, deliveries by quarter, the chart's December point and floor) reproduced from the bundle. The pad is the surface the 2026 surveys recorded with each area bare; P1 to P5 have exactly one bare survey each, P6's agree within 3 m3, so the pad is data-forced and the toe-plane and ring-lowest routes are contradicted by the bowls. Main call margin is thin but clean: every variant the judge ran stays at or above 3.4k t over the floor.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| P1 / P2 / P3 / P4 / P5 / P6 m3 | 32k/32k/29k/28k/24k/21k | 32,386 / 31,827 / 29,294 / 28,235 / 23,784 / 21,362 | yes |
| P1..P6 t | 29k/28k/26k/26k/21k/20k | 28,856 / 28,358 / 25,866 / 26,230 / 21,001 / 19,845 | yes |
| Reserve | 150,000 t | 150,157 t | yes |
| Days of cover | 62 | 61.78 | yes |
| Margin over floor | 4,000 t | 4,331 t unrounded | yes |
| Receipts COL / POL / USA | 144k / 286k / 176k | 143,980 / 285,944 / 175,934 | yes |
| Deliveries Q1..Q4 | 218k / 112k / 43k / 217k | 227,248-8,890 etc. = 218k / 112k / 43k / 217k | yes |
| Chart Dec 2026 point, floor | 150,000 t, 146,000 t | reproduced | yes |
| Toe-plane route | 138,000 t (57 d) | about 139k (57 d) | call reproduced, figure within 1k |
| "Lowest point around each pile" | 139,000 t (57 d) | not reproduced (judge's percentile reading gave 156k) | no (see below) |

## Competing answers that survived
None on any graded figure. Residual (not failing): PR-07 3.2 never defines "the yard pad", so the bare-surface reading rests on the surveys alone; that is the estimand choice and the intended analytical step, not an unpinned word. Intermediate chart points rely on extending the last-density rule to each survey; no gated figure depends on them.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 27 (unzip count; judge counted 26, metadata says 27) | yes |
| Formats | 3+ | 5 (csv, asc, xyz, xlsx, pdf) | yes |
| Big file | 25,000+ rows | historian 76,608 rows, xyz 40.5k rows | yes |
| Distractors | 2+ in metadata, none labelled by file name | boiler_bunker_levels, coal_cargo_analyses; names do not label them; each excluded by a shipped fact (PR-07 s.2) or asked-for figure unaffected | yes |
| Distractor weight | unused, weighs, does not answer a graded quantity | bunkers 2,453 t cannot carry the call | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, svg), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | pile table, receipts by coal, deliveries by quarter, chart; unit and rounding in prompt | yes |
| Prompt shape, 25+ criteria | identifiable, 25+ | "other" per metadata; 6 piles x 2 + reserve, days, call, 3 + 4 flows, chart items clears 25 | yes |
| Not LLM generated, goldens real | | judge found provenance clean, real irregularities; prompt 763 chars, one paragraph | yes |

## Gate G reconciliation
Thread: mechanism estimand_selection, family method_or_model_selection, surface_read_dependency no, sole_data_defect no. Design note and card: stump_class analytical; default path is a toe plane (138,000 t, 57 days, nominate), decisive step each area's pad from its own bare survey across both contractors (note's Rung 3, 149,846 t, 61.65 d); "No decoy" states nothing is planted. Match. The declared distractors (bunkers, cargo analyses) were not named by the thread as carrying the task; no surface read carries it. No Gate G finding. The thread's 150,157 t differs from the note's 149,846 t by 0.2 percent; every graded bin and the call agree.

## Gate H reconciliation
Thread: domain pass, layers pass, decisive_step analytical. Card analyst_test (toe plane, 57 days, nominate) and domain_test (stockpile inventory against a conformed pad) match the thread's easy route and swap test; Layer 1 items (grid/datum handover, kg/m3 vs t/m3, counter reset, historian catch-ups) are the same ones the note puts outside the stump. No mismatch.

## Stump power (Gate F)
Strong on the main call. The thread did not class the step analytical merely because the toe plane is the field's standard; it found the toe route contradicted by the data and the correct pad reachable only by comparing surveys across months and contractors. A solver who finds the bowls via the bare surveys lands the call, so the pair stays decided by the ladder's rung 3 vs rungs 0 to 2; the receipts and deliveries asks add independent traps. Main thread to weigh against the note's ladder.

## Findings, ranked
1. (Minor, optional) The "lowest point around each pile, 139,000 t" figure is not reproduced by the judge. It appears in submission.md section 1 (Final Recommendation, the "Not ... the lowest point around each pile, 139,000 t (57 days)" clause), and in the design note's Ladder (Rung 1: "139,217 and 137,883 t", lowest or mean level of the ring) and Survivor anatomy / fork table R1. It is not a Critical Component, Solution Step or Deliverable Answer, and no golden file carries it. It is a description of a rejected route whose number depends on how "ring" and "lowest" are defined (the judge's percentile reading gave 156k, and the toe plane gave about 139k vs the stated 138k). Risk: a reviewer who tries the route and does not get 139,000 t may flag the recommendation text. Cheapest fix: drop the clause or the figure from section 1, or state its construction (ring width, lowest cell versus percentile); keep the toe-plane statement.
2. (Info) Judge counted 26 files, the unzip has 27 (metadata correct); xlsx zip entries are dated 1980 (toolchain signature), cosmetic.

## Next action for the author
Remove or define the "lowest point around each pile, 139,000 t" clause in submission.md section 1 (graded numbers unaffected), rebuild only if a golden changes (none does), then proceed to ship; no re-judge needed.
