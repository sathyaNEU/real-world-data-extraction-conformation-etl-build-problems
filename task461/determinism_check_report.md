# determinism-check report, task461, 2026-10-15

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** FIX_NOW (solution text only: the per-cycle rounding order)
**Stumping type:** mechanism: forecasting (long-record adjustment of a short record, plus etl_conformance), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The judge thread (sonnet, medium, isolated to /tmp/determinism-check-task461-1792075541/target/) recomputed every graded figure from the bundle and reproduced them. $20 is the lowest setting within 300 days (275; $15 gives 323). All hub-record-through-the-overlap estimators land on $20. The one reachable wrong route is the node's own 336 days, which gives $15 (266). The files separate the two: 34 per cent of the hub's 2026 days are under $8 against 11 to 16 per cent in an ordinary year. The only fix is wording: net per cycle is $31,339 on unrounded cycles (88.0086) and $31,338 on the displayed 88.01. Say which in the solution steps.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Hub days / node days | 2,863 / 336 | 2,863 / 336 | yes |
| Ratio, 323 days, through origin | 2.21 | 2.2097 (OLS 2.23, median ratio 2.21) | yes |
| Expected days $5 to $40 | 365/355/323/275/224/176/138/113 | identical | yes |
| 2026 share of days under $8 | 34% | 34.3% (2019 to 2025: 11.0 to 30.6%) | yes |
| Monthly Full Cycles, Jan to Oct | 7.95 ... 2.99; 88.01 | identical; unrounded 88.0086 | yes |
| 27 stale-BMS hours replaced by meter/0.975 | total 88.01 | without them 81.36 | yes |
| Monthly DAM net ($k) | 268.9 ... 63.5; 2,758.1 | identical | yes |
| Net per cycle | $31,339 | 2,758,095.9 / 88.0086 = 31,339; on 88.01 gives 31,338 | yes, rounding order unstated |
| Conformed CSV rows | 3,199 | 2,863 + 336 = 3,199 | yes |

## Competing answers that survived
1. Main call: "expected 2027 cycling days" does not say whether to use the node's own year or the long hub record. Node-own gives $15, the long-record relation gives $20. The shipped hub record separates them (2026 low-spread share is an outlier, 2020 shows a similar year reverting in 2021). Residual risk is low to moderate. A persistence-weighted blend (half 2026, half history) puts $15 at about 300, which is a knife edge only under an unfiled persistence assumption.
2. Ask level (cycles, net per cycle): Schedule 4.3's "BMS record is unavailable" is not defined for rows that exist but show zero with the state held. A strict reader who counts only missing rows gets 81.36 cycles and about $33,900 per cycle. The held state of charge and about 95 MWh at the meter make the golden reading the expert one. Classified as an ask-level semantics risk, not a main-call fork.
3. Net per cycle rounds to 31,339 or 31,338 depending on the cycle figure divided.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | yes |
| Formats | 3 or more | csv, pdf, xlsx | yes |
| Large file | 25,000 or more rows | 68,712 (hub file) | yes |
| Distractors | 2 or more in metadata.json, none labelled in a file name | RTM prices and ancillary service prices (about 29k rows each), unused by the solution | yes |
| Distractor relevance | weighs but does not answer a graded quantity | judge found both present and unused; the design note says deleting either leaves the call and every ask unchanged | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, csv), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | menu table, monthly cycles, monthly nets, net per cycle, chart, conformed file; units and rounding in the prompt sentence | yes |
| Prompt shape and rubric | shape identifiable, 25 or more criteria | shape 04 identified; the rubric is portal-generated and not countable here, though about 33 separately gradable figures are asked for | yes (not countable here) |
| Not LLM generated, goldens real | no tells | judge found no authoring or benchmark language and coherent in-fiction dates; golden realism was checked at stage 3 | yes |

## Gate G reconciliation
Thread: mechanism forecasting plus etl_conformance, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_class analytical, with an analyst_test (the node's own days give $15, hub raw $10, hub plus premium $30, none gives $20) and a domain_test (a method swap moves the call). These match the design note's stump sentence. The declared distractors (RTM prices, ancillary service prices) carry nothing. The judge named no declared distractor as the surface read, so there is no too-load-bearing finding. No mismatch.
Gate G: no shipped artifact ranks the thresholds wrongly; the wrong routes sit in analyst choices, not files.

## Gate H line
domain: pass | layers: pass | decisive_step: analytical. Layer 2 is carrying a short record through a long correlated source's relationship and testing the 2026 regime against history. Swap test fails for other nouns. The design note's Three rules agree.

## Stump power (Gate F)
Good. The wrong answers are specific ($15, $10, $30) and reachable by a strong model that cleans everything and reads the policy correctly. The right answer needs an adjustment of a short, atypical record and a 323-day relation fitted away from the 13 hub-priced days. The judge estimates a plausible GPT failure through the node-own route.

## Findings, ranked
1. Per-cycle rounding order is unstated (31,339 against 31,338). Solution text only.
2. Residual main-call fork: node-own record against long-record extension. Closed by shipped data, so low to moderate risk. If the author wants it tighter, file the WHAT (the population is every 2027 operating day under weather the hub record shows) and not the HOW.
3. Ask-level reading of "BMS record unavailable" for zero-energy held-state rows. Not a main-call fork.

## Next action for the author
In submission.md step 9 (and the xlsx note if one exists) state that net per cycle divides by the unrounded January to October Full Cycles (88.0086), giving $31,339, and then re-run precut and figures_check. No prompt, input or golden-figure change, and no re-judge is needed unless that edit touches anything else.
