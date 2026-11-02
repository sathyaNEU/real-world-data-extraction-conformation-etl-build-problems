# determinism-check report, task467 (architecture 2, run a2), 2026-11-02

## Verdict
NOT_DETERMINISTIC (supplementary side only, Gate C). The main recommendation (GBP 127,785; February, March, April) is forced and reproduces exactly. No SOLUTION_WRONG.
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection (pairing rule chosen by validation on labelled openings), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

target.zip md5 cb252556972e11e3389478083d3b5f04; thread scratch /tmp/determinism-check-task467-a2/; verdict at /tmp/determinism-check-task467-a2/verdict.md.

## Why
The refund side is closed by the assurance (para 3: payment-run date, reissue date, day 0 = UK scan day, day 15+ late). Each refunded parcel's scan day is recoverable only by replaying openings against arrivals; the newest-waiting rule is validated on 181,318 of 181,318 labelled openings (arrival order 1,759), so it is data-forced. Two supplementary cells are open under the literal text:
1. Voucher month zone. `issued_at` is UTC and neither the prompt nor para 2(e) pins a zone. UTC month gives March 9,837 and April 1,570; UK month gives March 9,832 and April 1,575 (golden). One boundary voucher (2026-03-31T23:50:16Z, value 5). Two cells of ask 1's last column.
2. "Slow refunds" in the category count. Golden counts all 3,825 "Refund delay" vouchers in H1. A strict "the refund was actually late" reading excludes one voucher (case order refunded on day 14, 27 May, value 7): 3,824, one category moves by 1 voucher and about GBP 7.
The design note's fork table closes both (SF16 "UK time", SF17 "same set (asserted)") but the closure lives in the note, not in shipped text, and SF17's "same set" does not hold on the data.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Newest-first matches on labelled openings | 181,318 / 181,318 | 181,318 / 181,318 (either tie order) | yes |
| Arrival-order matches | 1,759 | 1,759 | yes |
| 2025 late refunds on replay | Feb 615, Dec 889 | Feb 615, Dec 889 | yes |
| 2026 refunds made by month | 14,103 / 15,546 / 18,301 / 13,300 / 12,894 / 13,497 (87,641) | same | yes |
| Late by month | 0 / 1,106 / 5,292 / 1,935 / 151 / 35 (8,519) | same | yes |
| Shares | 0.0 / 7.1 / 28.9 / 14.5 / 1.2 / 0.3 | same | yes |
| Payment | GBP 127,785 | 8,519 x 15 | yes |
| Voucher value by month (UK month, EUR 0.86) | 3,325 / 16,561 / 9,832 / 1,575 / 1,229 / 1,023 | same under UK month; March 9,837 and April 1,570 under UTC month | yes, one reading |
| Category table (case order) | 1,523/11,117 ... 275/1,922 (3,825) | same | yes; 3,824 under a strict reading |
| FIFO alternative | GBP 189,330, Feb and Mar | 12,622 late, GBP 189,330 | yes (the easy route) |

## Competing answers that survived
- Voucher month, UTC versus UK time: March 9,837 / April 1,570 against golden 9,832 / 1,575. No shipped sentence closes it (the assurance fixes UK time only for the goods-in scan).
- Slow-refund vouchers, all "Refund delay" reason (3,825) versus only those whose refunded order was actually late (3,824). The prompt does not define "slow".
- Category order join (voucher's own order versus case order): judge treats as closed by the data (36 per cent of own-order fields have no refund), a data-semantics pick but not an open fork.
No competing answer survives on the main call.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 12 | yes |
| Formats | 3+ | 4 (csv, parquet, pdf, xlsx) | yes |
| Large file | 25,000+ rows | 595,609 (orders parquet); also 334,172 and 325,616 | yes |
| Distractors | 2+ in metadata.json, none named by file name | 3 named (daily operations xlsx, shift rota, 2025 returns review pdf); file names do not label them | yes |
| Distractor behaviour | unused, weighs, ruled out by a shipped fact | thread confirms present and unused; the review pdf supplies headcount and parcel totals; arithmetic that answers a graded quantity was not separately tested by the thread | yes, not fully evidenced |
| Deliverables | 1 to 3, all in golden | 2, both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | monthly 5-column table, category x 2 table; prompt states whole numbers, per cent to one decimal, pounds to the nearest pound | yes |
| Prompt shape and rubric 25+ | identifiable, 25+ | shape 08; 30 monthly cells + 12 category cells + call and chart parts, so 25+ is supported; the rubric itself is not shipped here | yes (inferred) |
| Prompt form | under 1,000 chars, one paragraph, no data count | 977 chars, one paragraph, no count | yes |
| Not LLM-reading | | thread found no authoring disclosures, timeline coherent | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: Gate G method_or_model_selection (arrival-order pairing against the picking behaviour the labelled returns measure); card `stump_class: analytical`. These match. The thread did not name a declared distractor as the surface read carrying the task (distractors are the ops sheet, rota and 2025 review; none yields the pairing). The note's analyst test (FIFO files GBP 189,330 with Feb and Mar) is the same easy route the thread computed. No mismatch.
Gate G line: method_or_model_selection / analytical_non_defect / surface_read_dependency no / sole_data_defect no. Passes.

## Gate H reconciliation
Thread: `domain: pass`, `layers: pass`, `decisive_step: analytical`. Card and note: domain test is the record-linkage model validated on labelled links; Layer 2 estimation_fit; decisive step analytical. These match. The decisive step is a method chosen by validation on holdout labels, not the field's textbook method applied without judgment, so there is no "landable call" flag. The note's "Not rule application" line holds: the assurance files the WHAT only.
Gate H line: domain pass, layers pass, decisive_step analytical.

## Stump power (Gate F)
Strong on paper. The 2026 scan day is not stored (labels mostly blank). FIFO reproduces none of 2025's labelled late refunds and files GBP 189,330 with two breach months against the golden three. A solver must test pairing rules on the labelled openings and replay from 2 December 2024. The fix below does not touch this.

## Findings, ranked
1. Voucher month zone unpinned in shipped text (underspecified_objective, ask 1 last column, 2 cells). Note's SF16 closes it only inside the design note.
2. "Slow refunds" undefined for the category count; the note's SF17 "same set (asserted)" is contradicted by one voucher (3,824 against 3,825). Either the assert is wrong or the definition needs filing.
3. Category join via the case's order (SF18) is a data-semantics pick, closed by the data; not a fork, but the golden's table depends on it.
4. Distractor behaviour is thinly evidenced by the thread (no arithmetic test that a distractor reproduces a graded figure).
Fix with WHAT, not HOW: file the population and zone, not the pairing method, so the main-call stump stays untouched.

## Next action for the author
In `generator/` file two clauses in shipped text: the calendar month of a voucher's issue in UK time (prompt, or para 2(e) of the assurance), and what counts as a slow-refund voucher (all vouchers issued with the reason "Refund delay", or the strict reading, with the golden and `checks.py` SF17 assert set to match, 3,825 or 3,824). Rebuild twice for byte identity, re-run the free gates, then re-judge once. No data file and no main-call text changes.
