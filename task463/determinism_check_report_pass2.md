# determinism-check report, task463 (pass 2), 2026-10-31

## Verdict
DETERMINISTIC (main call and asks 2 and 3 reproduce); one supplementary fork on deliverable-file answer 1 (CSV row scope).
**Disposition:** FIX_NOW
**Stumping type:** mechanism: decomposition, stumping_family: method_selection, surface_read_dependency: no, sole_data_defect: no

## Why
Judge thread verdict: /tmp/determinism-check-task463-pass2/verdict.md (one thread, no retry; the thread read only the scratch bundle).
The main call (13 of 16 move; Pasta and rice, Cheese, Chocolate and sweets stay) is reached by a direct Sep 2025 vs Sep 2026
Tornqvist comparison and matches GEKS, direct Fisher and Laplace-share variants. Chain-linking gives 5 movers and ends below every
line's own change in nine items, so the thread did not treat it as a defensible literal reading. The CSV ask ("each product-month
of the items' lines") competes with "the lines compared": 13,156 rows over 1,012 lines against the golden's 14,364 rows over
1,172 lines. This fork is new in this reship (prompt reworded); pass 1 had no such finding. It touches one deliverable answer only,
not the call.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Lines compared per item (16) | 62,75,67,77,66,62,43,87,60,50,87,37,41,56,43,99 (1,012) | same | yes |
| Lines / line-months in the CSV | 1,172 / 14,364 | same | yes |
| Direct Tornqvist 12-month rates | 1.4,2.6,4.7,2.7,1.7,-0.2,1.4,-0.3,5.6,1.7,2.2,0.6,1.7,2.6,2.6,2.5 | same | yes |
| Published rates (12-month rates, Sep 2026) | 1.1,1.8,2.4,2.6,1.4,2.7,1.4,2.5,5.8,1.4,2.3,0.7,1.2,2.6,2.5,2.4 | same | yes |
| Differences, max moving gap / min staying gap | 0.8 / 2.3 | 0.82 / 2.32 | yes |
| Coverage (16 items) | 68,58,67,77,55,69,59,73,59,62,57,60,58,60,66,73 | same | yes |
| Chained rates (the competing reading) | 5 movers | 1.6,-3.6,2.9,-2.6,1.9,-0.2,1.5,-5.3,-0.9,-3.6,-4.9,-4.0,1.4,-5.8,-3.7,-4.2 | n/a (wrong route) |

## Competing answers that survived
1. CSV scope: all classified lines of the sixteen items (1,172 lines, 14,364 rows, golden) against lines compared only (1,012 lines, 13,156 rows). The shipped closure is none: the prompt's "lines" is read against "each item's lines compared" earlier in the same sentence. Fix: one clause fixing the population, not a count.
2. Construction, direct against chained: closed by the plan's "change in the item's prices over the year" and the line-bound check. Not a semantic gap; it is the intended method choice (declined to be filed, see the design note).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 13 | yes |
| Formats | 3+ | 5 (sqlite, csv, txt, xlsx, pdf) | yes |
| Large file | 25,000+ rows | sqlite 287,409; Wrenfold 28,266 (metadata says 29,280, thread counted 28,266 data rows; header or resend-row convention, minor) | yes |
| Distractors in metadata.json, none labelled by file name | 2+ | 3 (field quotes, retail sales index, delivery log); names carry no label | yes |
| Distractors unused yet weighable | yes | thread found all three present and unused by the solution; delivery log newly demoted after the timeliness ask was cut | yes |
| Deliverables | 1 to 3, all in golden | 3 (xlsx, png, csv), present in golden/ | yes |
| Asks multi-dimensional with unit and rounding | yes | per-item tables of 16 items; rates and differences to one decimal, coverage to whole per cent | yes (CSV ask has no rounding stated for unit price, minor) |
| Prompt shape; rubric 25+ criteria | identifiable, 25+ | 16 items x several columns, chart, CSV: well over 25 gradable figures; the rubric itself is generated and not inspected | yes (assumed) |
| Prompt | one paragraph, under 1,000 chars, no count | 855 chars, question first, no count | yes |
| LLM-read / realism | none | thread found none | yes |

## Gate G reconciliation
Thread: mechanism decomposition, stumping_family method_selection, surface_read_dependency no, sole_data_defect no. Design note (Pass 2 of the prior round) and card: stump_class analytical, the default path (linked monthly Tornqvist) lands on 5 movers instead of 13. These match. The thread did not name any declared distractor as the surface read. No mismatch.
Gate H: domain pass, layers pass, decisive_step analytical. Design note and card agree (domain_test: index compilation from transaction data with stockpiling drift; analyst_test: the linked route files five movers). The thread reached the golden by testing the chain against line-level bounds, a judgment the data had to settle, so it is not a landable-by-method-name call; Gate F is moderate to strong, consistent with the note's ladder.

## Stump power (Gate F)
Strong enough on paper: the chain-linked route that "compiled monthly" invites files Bread, Pasta and rice, Yoghurt, Butter and spreads and Fruit juice instead of thirteen, and the drift is data-native (offer-month stock-up). A solver who uses a direct or multilateral comparison lands the call, as the thread did.

## Findings, ranked
1. CSV row scope fork (prompt_ambiguity; deliverable answer 1 only): "each product-month of the items' lines" can be read as the lines compared. FIX_NOW in prompt.txt.
2. metadata.json `prompt_shape` still describes "each supermarket's timeliness" though that ask was cut; stale text, correct it.
3. Wrenfold's annual-return category codes differ from the map's codes (G110 is Coffee in the return, Bread in the map); matching by name works but is nowhere stated in a shipped file (minor ask-3 semantic risk, the thread did not class it exclusion-level). Note the reship removed the describing files; confirm the plan's section still tells the solver to match by name.
4. metadata.json row count for the Wrenfold file (29,280) differs from the thread's 28,266 data rows; confirm the generator's row definition.

## Next action for the author
Edit prompt.txt with one clause fixing the CSV population as every supermarket line classified to the sixteen items, not only the lines compared (no count, under 1,000 chars, re-run voice-check.py), correct the stale `prompt_shape` in metadata.json, rebuild twice byte-identical, rerun the free gates and re-judge once; goldens and the call are unchanged.
