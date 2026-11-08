# determinism-check report, task458 (architecture 3, run a3), 2026-11-02

## Verdict
NOT_DETERMINISTIC, on ask 7 only (net value invoiced by division, 2025). The main recommendation and asks 1 to 6 are forced and reproduce. No SOLUTION_WRONG.
**Disposition:** SEND_BACK (the judge's label). It touches only the supplementary ask layer; see Findings for the scope.
**Stumping type:** mechanism: binding_constraint, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
AHL's 262 PRICE (July price credit) rows each carry the item code of the order's first line, a header artifact. The golden instead places each credit on the order's lines charged above the customer's pre-April price, which equals those lines' overcharges to the penny on all 262 rows. No shipped file and not the prompt says to place credits that way. A literal reader who nets each ledger row on its own item's division gets a different defensible ask 7 (Kitchen and Dining 40,977,000 against 41,162,000; Garden and Outdoor 25,137,000 against 25,081,000). Gates C and E fail for ask 7, taxonomy competing_defensible_answer. The main call is robust: the provision stays 5.17 to 5.21M across plausible variants and the shortfall rounds to 0.5M in every variant.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Excess AHL / AHI / AHB (GBP) | 5,080,000 / 500,000 / 1,430,000 | 5,075,960 / 499,414 / 1,427,747 | yes |
| Total excess | 7,000,000 | 7,003,121 | yes |
| Valuehall closing stock | 200,000 | 198,865 | yes |
| Stock at cost | 44,600,000 | 44,602,438 | yes |
| Valuehall proceeds / cost | 0.617 | 0.6166 | yes |
| Daily sales at cost, stocked weeks | 1,377 | 1,376.8 | yes |
| 2027 through Valuehall (1,801 days) | 2.48M | 2.48M | yes |
| Trade-lot price / cost | 0.102 | 0.1016 | yes |
| Provision / inventories / base / drawn / shortfall | 5.2 / 39.4 / 24.6 / 25.12 / 0.5 (M) | 5.19 / 39.41 / 24.63 / 25.12 / 0.49 | yes |
| 2025 net units by division | 11,743k; 7,603k; 7,616k; 6,215k; 2,874k | match to 1,000 | yes |
| 2025 net value, golden credit basis | 41,162k; 33,105k; 36,168k; 29,568k; 25,081k | match to 1,000 | yes (only under the unfiled credit placement) |

## Competing answers that survived
- Ask 7, price-credit placement. Credit on the PRICE row's own item (literal ledger reading) against credit on the order's lines charged above the pre-April price (golden). Both reproduce from the files. Nothing shipped or in the prompt closes it.
- Main call: none survived.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 18 | yes |
| Formats | 3 or more | csv, xlsx, pdf | yes |
| Large file | 25,000 rows or more | AHL_sales_order_lines 50,054 lines, AHB 29,566 | yes |
| Distractors | 2 or more in metadata, none labelled in a file name | AHL_open_purchase_orders_2027, dc_pallet_occupancy_2026; neither name labels a distractor | yes |
| Distractor weight | unused, relevant, ruled out by a shipped fact | stated in metadata (FIN-07 2.5; space not value); not checked for arithmetic reproduction of a graded quantity | yes, light check |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pdf), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | stated in the prompt sentence for each | yes |
| Prompt shape / 25 criteria | identifiable, 25 or more | not countable here: the rubric is generated downstream | not verified |
| Reads as real work product | no LLM tells | judge found none | yes |

## Gate G reconciliation
Thread: mechanism binding_constraint, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Gate H: domain pass, layers pass, decisive_step analytical. Design note: Layer 2 allocation_constraints (capacity), decisive step is seeing that Valuehall's sales follow its store count and not what it was sent, so the surplus beyond the stocked trade days is valued at trade prices; the not-semantics line is the same easy route (0.617 on everything, GBP 2.8M, no waiver). Thread and note agree on the stump and easy route. The mechanism label differs in wording only (binding_constraint against allocation_constraints, one family). The thread did not name either declared distractor as a surface read. No mismatch.

## Stump power (Gate F)
The decisive step is a demand-limited channel's throughput estimate, and the easy single-rate route files a wrong call (no waiver). The thread did not class the step as a standard-method landing. The shipped lot register and the 2023 episode are the evidence and nothing states the conclusion. One thin spot: the non-promotion ratio 0.628 with a daily rate of 1,390 gives 5.14M, rounding to 5.1M (shortfall still 0.5M). Breakeven provision is about 4.41M, a 0.78M margin on the waiver call.

## Findings, ranked
1. Ask 7 is not determinate (credit placement unfiled). Scope: the supplementary device only. It does not touch the decisive step or the main call, which stay frozen. The SEND_BACK is therefore a repair on the ask layer, though any prompt change alters what solvers read, so ask 7 must be re-judged once.
2. Rounding thin spot above on the provision (5.1 against 5.2 under one variant pairing), worth a check against the filed method.
3. AHI archive pre-July-2025 case lines are detectable only from unit-price jumps; the last case day is 4 July, not 1 July (data-detectable, Layer 1).

## Next action for the author
In the generator, either file the WHAT of ask 7 in the prompt (each price credit counted in the division of the lines it corrects), or post each PRICE row on an overcharged line's item so the literal ledger reading equals the golden; keep the filed WHAT free of the HOW. Rebuild twice byte-identical, then re-judge ask 7 once.
