# determinism-check report, task451, 2026-10-13

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection (completion of the open service months under a change in the payment process), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
One isolated thread (Sonnet, medium) saw only a fresh unzip of `target.zip`, the prompt and the submission's graded blocks, with the reviewer's system prompt inlined verbatim. It read the files literally first. Schedule B, B.1.4 counts claims "whenever the claims are paid", and B.3.1 has the Fund estimate the claims not yet paid, so the paid-through-January figure must be completed. The method is open and the data separate the candidates: receipt to payment fell from a median of 23 days to 1 at the 5 October 2026 move to Tallis, while service to receipt held. A paid-date chain ladder over 2025 and 2026 names nine partners. No completion names two. Every received-date development, and a paid-date ladder restricted to the payments after the cutover, names the same four (Stonecrest, Bellmont, Kettle Run, Harrow Point).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Receipt to payment, first versions, received before 5 October 2026 and after | 23 and 1 days | 23 and 1 | yes |
| Service end to receipt, received in 2025 | 13 days | 13 | yes |
| Service end to receipt, after | 14 days | 13 (received in 2026) | note: the write-up now says "received from 5 October 2026" (14 on the build) |
| Members over $200,000 | 7 | 7 | yes |
| The four owing partners' share of target | ranges across four completions | lower ends exact; the post-cutover paid ladder on latest versions ran 1.6 to 1.8 points above the upper ends | note: ranges now stated over the three received-date developments, recomputed by `verify.py` |
| Others under the line | under 102% | at most 97.0 (received date), 101.6 (its post-cutover paid ladder) | yes |
| Paid-date ladder, all of 2025 and 2026 | nine partners | the same nine | yes |
| Pharmacy, twelve partners, to the thousand | stated | all twelve | yes |
| Outside share, twelve partners, one decimal | stated | all twelve (billing NPI against the group NPI) | yes |

## Competing answers that survived
None on the main call. Two notes on the asks, both closed in the generator after the pass:
- Ask B: the clinician roster with its "with partner since" dates gives other shares (0.5 to 2.3 points), all from services billed under the group NPI by clinicians no longer on the 1 January 2027 roster. The judge rated the billing reading better evidenced (borderline-accepted). The roster now says in its own header that a clinician who leaves a group is removed when the partner gives notice, so it cannot answer for a service given before a departure.
- Ask A: counting only reversals processed by 31 December 2026 moved Ashby Lane (546 against 543 thousand). The judge rated the netted reading literal. B.4.1(a) now says "reversals included whenever processed".

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 11 | yes |
| Formats | 3 or more | 5 (csv, pdf, docx, xlsx, txt) | yes |
| Large file | 25,000 rows or more | claims extract, 174,248 rows | yes |
| Distractors | 2 or more, named in metadata.json, none in a file name | stop-loss policy summary, quality scorecard | yes |
| Deliverables | 1 to 3, every one in the golden | partner_settlement_2026.xlsx, partners_against_target_2026.png | yes |
| Asks | multi-dimensional, unit and rounding stated | 12 owes rows, 12 pharmacy figures to the thousand, 12 shares to one decimal, the chart | yes |
| Realism | nothing reads as generated | judge and reader: none | yes |

## Gate G reconciliation
The thread's mechanism (method_or_model_selection, the development basis under a payment-timing change), family (analytical_non_defect) and its Gate H line (domain pass, layers pass, decisive step analytical) match the card (`stump_class: analytical`, `gate_g: method_or_model_selection`, `stump_strategy: maturity_censoring`) and the design note's decisive step. It named no distractor as the surface read; it read the stop-loss deductible as a near miss against B.1.5, as designed.

## Stump power (Gate F)
Good, moderate to high (the thread): the textbook paid-date chain ladder names nine, no completion names two, and connecting the release note to the ladder's diagonals and choosing the received-date triangle is real analysis.

## Findings, ranked
1. The post-cutover paid ladder was not specified closely enough to replicate its range ends (the thread built it on latest versions by paid date). Repaired: the critical components and block 1 state ranges over the received-date developments only (Stonecrest 108.9 to 109.4, Bellmont 107.1 to 107.5, Kettle Run 103.7 to 104.1, Harrow Point 103.2 to 103.7), the paid ladder is cited without figures, and the latest-version construction joined the golden family with the targets placed against it (Ashby Lane at most 100.9 on any golden route).
2. "14 after" read as received in 2026. Repaired: "14 for claims received from 5 October 2026".
3. The two ask notes above. Repaired in the roster header and B.4.1(a).

## Next action for the author
None: ship. The repairs moved no call and no owed ask figure (`checks.py` 168 assertions and `verify.py` green on the final build).
