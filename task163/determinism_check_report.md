# determinism-check report, task163, 2026-11-02

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting (counterfactual claims rate carried onto a changed layout; etl_conformance in the asks), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread: one isolated sonnet judge thread (scratch /tmp/determinism-check-task163-1793635898/, verdict.md there). target.zip md5 f93b5359c7f42306aa58070549a8c58b.

## Why
Schedule 3 s3.2 fixes the count (validated "Wrong item received" claims by despatch date, per 10,000 order lines). The claims' own pairs, location_master.csv and the plan's Faces 2027 sheet then leave one exposure model. Under the re-slot, 2027 claims are 3,807 (about 3,800), 3.70 per 10,000 against the limit of 2.5. Today's layout gives 1,755 claims, 1.70 per 10,000. Every golden figure reproduced.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Baseline claims (register: Wrong item received, Validated, despatched 22 Sep 2025 to 20 Sep 2026) | 1,619 | 1,619 | yes |
| Order lines, 52 weeks (pick_velocity_by_week.csv) | 9,682,373 | 9,682,373 | yes |
| Share of picks beside a face within 15 g, now | 15.6% | 15.62% | yes |
| Claims per 10,000 such picks | 10.71 | 10.705 | yes |
| Share on the plan's faces, 2027 lines (10,302,650) | 34.5% | 34.52% | yes |
| Share on today's faces, 2027 lines | 15.9% | 15.91% | yes |
| 2027 claims under the re-slot | 3,800 | 3,807 | yes (to nearest 100) |
| Per 10,000, re-slot / today | 3.7 / 1.7 | 3.695 / 1.703 | yes |
| Agency hour cost, Sep 2025 to Aug 2026 (12 months) | 16.38, 16.37, 16.52, 16.32, 16.15, 16.15, 16.20, 16.77, 16.88, 16.86, 16.83, 16.84 | same | yes (premium fit 1.47000 and 2.35998, residual under 0.005 on all 15 lines) |
| Returns by family, Oct 2025 to Sep 2026 | Make-up 21.0/20.4/27,088; Skincare 16.3/28.8/26,512; Fragrance 25.8/23.5/23,931; Haircare 27.6/19.8/8,772; Bath and body 17.8/25.8/6,068 | 20.98/20.42/27,087.95; 16.34/28.85/26,511.97; 25.79/23.50/23,930.95; 27.63/19.78/8,771.67; 17.76/25.83/6,068.19 | yes (all 13 Ravelrig invoices reproduce to 0.00) |
| Chart figures (1.7, 1.7, 3.7, limit 2.5) | as main call | match | yes |

## Competing answers that survived
Main call: none. Forks the thread tested:
- Window by lodged date or including 1 to 21 Sep 2025: 1,605 or 1,707 claims. The contract counts by despatch date and the prompt gives the 52 weeks, so this fork is closed.
- Inclusive against strict 15 g: no difference. Every claim pair is within 10 g and none sits at exactly 15 g.
- Binary "any near neighbour" model: 3,094 claims, 3.00 per 10,000. The data refute it (claim rate 10.8 with 1 of 1 neighbours near, 10.6 with 2 of 2, 5.33 with 1 of 2).
- Adjacency within a bay only: 3,607 claims, 3.5. Refuted by the 7% of claims that cross a bay.
- Naive 1.67 scaling: about 1,700 claims, 1.7. This is the stump, not a competing answer.
- The call (hold the re-slot) is the same on every reading except the naive scaling.

Asks, one quiet fork: hour cost by week_commencing instead of the month the shift started (Sep 16.39, Dec 16.34, other months 0.01 to 0.1 off). The prompt does not say "by the month the shift started", but shift_start_date is the only per-shift date and "hour worked" points to it, so the thread rates it low risk. Other forks (billed hours only 15.8 to 16.5, invoice-month basis, Dec 16.79) are clear misses. Returns without the handheld grade swap: Bath and body repacked 20.0 (golden 17.8), Skincare 20.3 (golden 16.3). The invoices select the golden reading. First grade or every row also moves shares by 0.3 points or more.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | CSV, XLSX, PDF | yes |
| Large file | 25,000 or more rows | pick_velocity_by_week.csv 49,372, returns_grading_log.csv 60,898 | yes |
| Distractors | 2 or more in metadata.json, none named in a file name | picker_training_log.xlsx, aubrine_promotions_2027.csv; neither file name labels it | yes |
| Distractor behaviour | unused by the solution, weighable, ruled out by a shipped fact | Neither is used by the golden. The thread found nothing exclusion-level. No distractor answers a graded quantity (the plan's travel and hours-saved summary is stated, not a claims figure). | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pptx), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 12 months and 5 families x 3 measures, rounding in the prompt | yes |
| Prompt shape and rubric | identifiable shape, 25 or more criteria | Shape identifiable. About 27 graded ask figures plus the main call and its components. The rubric itself is not shipped, so I could not count it. | yes, by count of gradable figures |
| Realism | nothing reads as LLM generated | Thread found operational artifacts (procedures, SLA schedule, invoices, WMS exports) with realistic noise and coherent dates. I did not review golden realism beyond that. | yes |

## Gate G reconciliation
Thread: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical, with an analyst_test (1.67 scaled to about 1,700 inside the limit; look-alike multiplier 1,400 or 1,800; only the rate per pick beside a face within 15 g gives 3,800) and a domain_test (unrecovered error probability of a picking task). Design note `## Three rules` carries the same account and each of No decoy, Not semantics and Not rule application on its own line. These match. The thread names the naive per-line scaling as the surface read, not a declared distractor, so no distractor is too load-bearing.

Gate H (thread): domain pass (picking accuracy and a slotting-driven error rate against an SLA), layers pass (Layer 1: two layouts, location formats, a mid-year capture change, re-graded returns, lagged invoices; Layer 2: claim exposure by neighbour weight), decisive_step analytical. No mismatch with the card.

## Stump power (Gate F)
The thread rates it good. The easy route, volume scaling of 1.67 per 10,000, gives 1.7 under both layouts and approves the re-slot, so a careful analyst could still file the wrong call. The decisive step is an exposure model joined to shelf neighbours and carried to the plan's faces, not a stated rule. The asks add independent reconstructions. The premium rates (1.47, 2.36), the nine-day pay-period rule, the Ravelrig unit prices and the handheld grade swap are in no shipped document and are recoverable only by exact reconciliation (premium lines to 0.005, invoices to 0.00). That is demanding but unique, and the thread did not class it as missing data. A strong solver could land the main call and still lose ask weight. The main thread should weigh this against the design note's ladder.

## Findings, ranked
1. None blocking.
2. Optional: the hour-cost ask could say "by the month the shift started" (low-risk quiet fork, week_commencing gives 0.01 to 0.1 off in most months).
3. Information only: ask-side parameters (premium rates, the swap) are recoverable only by reconciliation. Unique, but it will cost solvers ask weight.

## Next action for the author
Proceed to ship. The optional pin of the hour-cost ask is the only change on offer, and it needs a rerun of the free gates if made.
