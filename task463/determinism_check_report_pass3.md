# determinism-check report, task463 (pass 3), 2026-11-01

## Verdict
DETERMINISTIC (no SOLUTION_WRONG)
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection (design note: estimation_fit, chain-linked aggregation), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judged bundle: target.zip sha256 e020250e6b38cfea06b6b019477646ff3fa3783771a74af67ac1b5c89eb5f5fa (matches the file on disk). One thread, derivation written before graded blocks were opened. Thread verdict: /tmp/determinism-check-task463-p3/verdict.md; derivation: /tmp/determinism-check-task463-p3/derivation.md.

## Why
Executing the plan's sections 3.3 to 3.6 and 4.1 word for word (matched lines sold in all 13 months, monthly unit value with GST, Tornqvist spending weights, 12-month rate Sep 2025 to Sep 2026) gives 13 items moving and Pasta and rice, Cheese, Chocolate and sweets staying. Nearest cases are 0.8 points (moving) and 2.3 points (staying) from the 1.5 line, so no knife-edge. Every ask reproduces.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Product-month rows / lines / lines compared | 14,364 / 1,172 / 1,012 | 14,364 / 1,172 / 1,012 | yes |
| 16 transaction rates (calc'd Sep25 to Sep26) | per submission block 2 | all 16 identical to one decimal | yes |
| 16 published rates and differences | per block 2 | identical (sheet 12-month rates) | yes |
| Moves | 13 move, 3 stay | 13 / 3 | yes |
| Breakfast cereals 2.6 vs 1.8, 0.8 | CC1 | 2.6 / 1.8 / 0.8 | yes |
| Pasta and rice 4.7 vs 2.4, 2.3 | CC2 | 4.7 / 2.4 / 2.3 | yes |
| Coverage, 16 items | 68,58,67,77,55,69,59,73,59,62,57,60,58,60,66,73 | identical; nearest .5 edge 57.04 (1221) | yes |
| Chained alternative | 5 move, nine items 4.6 to 8.4 below | 5 move (1101, 1105, 1145, 1151, 1223) | yes |
| GEKS vs direct | within one decimal | within 0.04 | yes |

## Competing answers that survived
None as a competing answer. Watch items:
1. Chained monthly Tornqvist (five items move). Closed by 3.6's estimand ("change in the item's prices over the year"), the plan's matched-line and weight rules, and the data (linked index ends below every line's own change in nine items). Residual risk: the design note itself says the plan "says nothing on how a month's index reaches back to September 2025", so a literal reader who values the "compiled monthly" phrasing could chain. The thread judged the gloss sufficient.
2. Wrenfold coverage rule (H1 read by recorded code, H2 by printed name). The returns sheet header says "by the category code each sale was recorded under ... Category names as in the current product hierarchy", which supports it, but the renumbering date is not stated and needs the weekly feed and unit-price consistency to reconstruct. A names-for-both reading gives different coverage for most items. Affects ask 3 only.
3. Published rate from the sheet versus ratio of rounded indices differs by up to 0.06 (1105 diff 2.3 vs 2.2); no call change.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10+ / 3+ / 25,000+ rows | 13 / 5 (csv, pdf, sqlite, txt, xlsx) / sqlite 287,409 rows | yes |
| Distractors | 2+, in metadata, not in file names | 3 named (field quotes, retail sales index, delivery log); names do not label them | yes |
| Distractor relevance | unused, weighable, ruled out by a shipped fact | Field quotes feed the published index; retail sales index is neighbouring; delivery log used only for resend checks. None reproduces a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 3 (xlsx, png, csv), all in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | scorecard, coverage, chart, product-month file; rounding in prompt | yes |
| Prompt shape / 25+ criteria | identifiable, 25+ | shape 10; design note records the rubric freeze check; criterion count not recomputed here | yes (by note) |
| Reads as real, not LLM generated | | resent weeks, stripped EAN zeros, returns, renumbered categories; no tells found by thread | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: estimation_fit (chain-linked aggregation), analytical stump, no decoy. Match. Declared distractors are not the surface read; the surface read (chaining) comes from the solver's habit, not a shipped artifact. Published index is correct for what it measures and ranks nothing. Gate G: CLEAN, no shipped artifact ranks the candidates wrongly. Distractor not load-bearing.

Gate H line: domain: pass, layers: pass, decisive_step: analytical (price-index construction under promotional stock-up; easy route chains the twelve comparisons and files five movers; Layer 1 mess is resends, EAN padding, fiscal weeks, returns, GST, renumbering). Matches the card/note (`domain_test`, `analyst_test`, Three rules).

## Stump power (Gate F)
Moderate. The thread notes that a strong solver who reads 3.6 literally and compares September to September lands the call, so the main-call stump rests on how many solvers chain. It also says the stump is "close to a rule reading" because 3.6 states the Sep-to-Sep estimand, kept analytical by the data-side evidence against the chain. Main thread to weigh this against the design note's ladder and the Part 1.1 stumping ladder (the note concedes the plan is silent on how the index reaches back, which is the opposite emphasis: possible tension between "plan silent" and "3.6 closes it"). Per the library, standard methods are textbook routes a strong solver takes.

## Findings, ranked
1. (Watch, moderate) Direct-versus-chained: determinism rests on the 3.6 gloss. Design note says the plan is silent on reaching back; judge says text closes it. Keep the gloss intact; any hardening must not weaken 3.6.
2. (Watch, low to moderate) Coverage ask 3 depends on inferring Wrenfold's renumbering from the weekly feed and unit prices; sheet header gives only an indirect hint. Main call unaffected.
3. (Stump power) Moderate; careful literal readers land the call.
4. (Nit) Chart rebasing of the published index to Sep 2025 = 100 is implied by the chart ask, not stated; no graded figure affected. Calderby per-row versus aggregate unit-price rounding differs by a penny in 7 of 3,930 product-months (CSV only).

## Next action for the author
No repair required. Proceed with the stage-4 ship checks; optionally add a golden-side note citing the weekly-feed cross-check for the Wrenfold H1 code reading.
