# determinism-check report, task307, 2026-10-27 (pass 2, the one re-judge after FIX_NOW)

## Verdict
DETERMINISTIC (not SOLUTION_WRONG)
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread: one sonnet/medium thread. The runtime had no Agent tool, so the brief was written to /tmp/determinism-check-task307-1793114444/judge_brief.md and the main session spawned the thread. Scratch unzip: /tmp/determinism-check-task307-1793114444/target/. Verdict: /tmp/determinism-check-task307-1793114444/verdict.md. prompt.txt is current (not the legacy prompt.md).

## Why
The shipped text fixes the estimand literally: scoring guidance 2.1 to 2.3 and 3.1, documentation 6.1 (user-equilibrium assignment of the AM and PM tables) and Table 4.2. Run that way, Center Street saves 322,911 vehicle-hours a year, more than twice Route 9 at 159,166, so the slot rule names TIP-28-009. The cost ranking agrees. All 8 AADTs, 8 K-factors and 12 validation percentages reproduce from the Count Manual 3.2 and 4.1 to 4.3, the Maintenance 2025 sheet and documentation 6.3 and 6.4. Pass 1's two unfiled conventions (FIX_NOW) are closed: the thread found no open fork except the single midnight-carry wrinkle below.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Center Street annual benefit / per USD 1M | 323,000 / 8,300 | 322,911 / 8,301 | yes |
| Route 9 | 159,000 / 3,400 | 159,166 / 3,401 | yes |
| Southport | 126,000 / 4,900 | 125,963 / 4,901 | yes |
| Ferry Street | 37,000 / 2,100 | 37,203 / 2,102 | yes |
| No-build link volumes vs loaded network file | n/a | within 0.05 vehicles, 23 links, AM and PM | yes (consistency) |
| AADT S-0101 to S-0108 | 77,018; 12,021; 19,396; 54,773; 36,800; 15,291; 13,859; 10,188 | identical | yes, all 8 |
| K-factor S-0101 to S-0108 | 0.126, 0.125, 0.138, 0.113, 0.112, 0.139, 0.115, 0.115 | identical | yes, all 8 |
| Validation, 12 cells | -5.5, -5.8, -13.3, -13.1; 0.0, -0.6, -2.6, -1.2; -0.1, 0.5, 2.2, 1.5 | identical | yes, all 12 |

The closest rounding boundary is 322,911 against 322,500. Fault onset at hour level or day level gives identical results.

## Competing answers that survived
- Fixed-volume re-timing at no-build volumes gives Route 9 196,483 (4,200 per million). It is not licensed: 6.1 and 2.1 name equilibrium on the build network. It is the intended wrong route, closed by shipped text.
- Residual soft spot (thread: "the only soft spot", treated as closed): a miss in hour 24 whose carried volume lands in hour 1 of the next day. Read as "not inside a running day", S-0101 AADT becomes 76,808 instead of 77,018, and S-0102, S-0104, S-0105 and S-0106 move by a few vehicles. Some K values move by 0.001 to 0.002. Manual 3.2 does not say "across midnight", but the data shows the carry (S-0101 EB 12/25 hour 1 is 685 against about 200 typical). The fix is optional and is already being taken: see Next action.
- Funding fit in 3.1 is unstated and no cost cap is shipped, so nothing contradicts it.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, parquet) | yes |
| Large file | 25,000 or more rows | 140,160 rows (ATR csv), 900,091-row parquet | yes |
| Distractors in metadata.json | 2 or more, none labelled in a file name | 5 named: crash summary, MRTA ridership, probe parquet, CMP reference csv, CMP reliability pdf; no name labels one | yes |
| Distractors unused yet weighable | unused; a shipped fact rules out any that answers a graded quantity | unused by the solution. The loaded network is not a declared distractor, but it reproduces the no-build run and is used by the golden. The fixed-volume wrong answer reproduces arithmetically from it and 6.1 rules it out | yes |
| Deliverables | 1 to 3, all in golden, no format family required | 2 (xlsx, pptx), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | every ask | 4 candidates x 2 metrics, 8 stations x 2, 12 direction-peak cells; rounding stated for every figure in prompt.txt | yes |
| Prompt shape and rubric | identifiable, 25 or more criteria | other (shape card), single paragraph of 798 characters. Graded figures: 8 + 16 + 12 + recommendation, components and brief, which is well over 25. The rubric itself is generated downstream and was not inspected | yes (by count of graded cells) |
| No LLM-generated read | all | judge saw agency-like artifacts (mixed date formats, DST 23/25-hour days, station swap, NR and EST statuses); no provenance leakage | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card and design note: stump_class analytical; the stump is the fixed-volume re-timing against equilibrium re-assignment, with Layer 1 mess (DST, station swap, NR and EST, carry polls) not carrying the stump. Match. The thread did not name a declared distractor as the surface read that carries the task. The competing answer comes from the loaded network file, which is a consistent reference, not a declared distractor. The thread noted the candidate descriptions "hint at Route 9's weaving"; the main thread is making the Route 9 sponsor description neutral, which removes that hint. Gate G: pass.

## Gate H reconciliation
Thread: domain pass (travel-demand modelling and TIP appraisal; swapping the nouns breaks it), layers pass (Layer 1: DST, station swap, NR, EST, carry-over polls, fault windows; Layer 2: equilibrium assignment with route switching and induced bottlenecks), decisive_step analytical, borderline rule_application. Design note `## Three rules` and the card's analyst_test and domain_test agree on domain, layers and decisive step. Divergence to note: the thread's borderline reading rests on 6.1 and 2.1 stating the equilibrium method outright, while the note argues that 2.1 files only the estimand and the documentation files assignment as its general method. The thread also reached the golden by running the equilibrium solve, not by applying a filed procedure with no judgment. This is the same shape as the "standard method" case: the equilibrium solve is a textbook route a strong solver takes, which bears on stump power.

## Stump power (Gate F)
Moderate to good per the thread. The shortcut (re-time at no-build volumes or the loaded network's volumes, filing Route 9 at 196,000) is attractive: the loaded network is shipped and the link edit is fast. The supplementary count and validation asks add independent hard layers. Risk: because 6.1 and 2.1 name equilibrium assignment, a careful reader is pre-warned, and a strong solver who runs the stated assignment lands the call (`stumping` 1.3). The main thread weighs this against the design note's ladder; the note's one data-native argument is that the record shows where traffic goes only under re-assignment. This report does not recommend a change to the filed text: the WHAT (assignment to equilibrium on the build network) is the estimand, and removing it would reopen the fork. Leave the ladder as is unless the main thread's paper argument says both of the top two responses land the call.

## Findings, ranked
1. No blocking finding. Every graded figure reproduced independently, and no rounding boundary is near.
2. Soft spot, optional: the manual 3.2 midnight-crossing carry. The thread treats it as closed by the carry visible in the data. It affects S-0101, S-0102, S-0104, S-0105 and S-0106 AADT and some K values, none of which touches the call.
3. Stump-power risk, not a determinism defect: equilibrium is stated in 6.1 and 2.1, so the decisive step is borderline rule_application (see Gate H).
4. The Route 9 sponsor description hints at weaving (thread, under stump power). Neutralising it is already planned.

## Next action for the author
Pass 2 approves; do not re-judge. The main thread has said it will take two optional edits: pin the midnight carry in manual 3.2, and make the Route 9 sponsor description neutral, with no figure moving. Keep these constraints.
- The 3.2 pin must say only that a carried poll counts "including across midnight". It must not call the carry-over a defect, and it must not file the method for the fault windows.
- The sponsor description must stay a plain description with no argument for either answer.
- These edits change the cut pack, so rebuild twice byte-identically, then rerun `verify`, `figures_check.py` and `leak.py` before the SHIPPED commit. The judge pass is not repeated.
