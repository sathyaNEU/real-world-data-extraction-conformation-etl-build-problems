# determinism-check report, task467 (pass 2, run a2b), 2026-11-02

## Verdict
DETERMINISTIC (minor SOLUTION_WRONG wording defect in CRITICAL_COMPONENTS 1 and step 3)
**Disposition:** FIX_NOW (wording only; no input file, figure or rerun changes)
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Every committed figure reproduced from target.zip (md5 cb252556972e11e3389478083d3b5f04). Each refund's delivery day is on no column; it is fixed by replaying goods-in scans and openings in time order, each opening (rejected parcels included) taking the newest parcel waiting. That matches 181,318 of 181,318 labelled openings; arrival order matches 1,759. The data, not a reading of the prompt, separate the candidates. Wording defect: the labelled openings run from December 2024 to 12 April 2026 (Jan 2026 1,658; Mar 1; Apr 844), not "2025 and January 2026". Label gap in Feb/Mar is untested, so newest-first there is an extrapolation, but it is the only candidate the data support.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Newest-first labelled matches | 181,318 / 181,318 | 181,318 / 181,318 | yes |
| Arrival-order matches | 1,759 | 1,759 | yes |
| Refunds made Jan-Jun (ledger RETURN, PAID; failed card at reissue) | 14,103 / 15,546 / 18,301 / 13,300 / 12,894 / 13,497 | same (87,641) | yes |
| Late refunds | 0 / 1,106 / 5,292 / 1,935 / 151 / 35 (8,519) | same | yes |
| Late share % | 0.0 / 7.1 / 28.9 / 14.5 / 1.2 / 0.3 | same | yes |
| Payment | GBP 127,785 | 8,519 x 15 | yes |
| 2025 late (Feb, Dec) | 615 / 889 | 615 / 889, other months 0 | yes |
| Voucher value by UK month (GBP) | 3,325 / 16,561 / 9,832 / 1,575 / 1,229 / 1,023 | same (UTC months would move Mar, Apr) | yes |
| Refund-delay vouchers by case-order category | Womenswear 1,523/11,117; Menswear 648/4,693; Footwear 621/4,537; Home 402/2,840; Kids 356/2,608; Accessories 275/1,922 | same (3,825) | yes |

## Competing answers that survived
None on the main call. Arrival order (GBP 189,330, Feb and Mar only), uniform pairing (GBP 192,000) and opening-day-as-delivery (GBP 0) all fail the labelled test or the assurance's goods-in wording.
Residual forks outside the main call:
- Ask 4: the voucher's own order_ref is the customer's latest order and differs from the case's order on 1,631 vouchers (36 per cent of those orders never refunded). Prompt says "orders in that category" without naming the order. The case order is supported by the files (every case order was refunded); a literal reader of the voucher row gets Womenswear 1,387 / 10,087 etc. Resolvable, not closed by prompt text. Optional one-clause pin ("the order the delay case was opened on") moves no figure.
- Voucher currency is inferred (customer order currency; redemptions at face value on matching-currency orders, zero cross); all-pounds would give 3,393 / 16,860 / 10,003 / 1,594 / 1,250 / 1,044. Forced by evidence, but semantics, in the CSV only.
- Rubric-level only: CSV column names and "met" form not pinned; chart line drawn at 5 per cent late share.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 12 | yes |
| Formats | 3+ | 4 (csv, parquet, pdf, xlsx) | yes |
| Large file | 25,000+ rows | 325,616 scans/openings; 595,609 orders rows | yes |
| Distractors | 2+ named in metadata.json, none labelled in a file name | 3 (daily operations xlsx, shift rota, 2025 review pdf); neutral names | yes |
| Distractor weight | unused by solution, weighable, ruled out by a shipped fact | per metadata and the judge's hygiene read; I did not recompute a distractor-derived answer | yes (not independently recomputed) |
| Deliverables | 1 to 3, all in golden | 2, both in golden | yes |
| Asks | multi-dimensional, unit and rounding stated | 6 months x 5 fields, category table; unit and rounding in the prompt | yes |
| Prompt shape and 25+ criteria | identifiable, 25+ | shape 08; graded cells (30 monthly, 12 category, payment, months) exceed 25; rubric is portal-generated, not checkable here | yes (inferred) |
| Reads as real | no LLM tells, goldens realistic | prompt 983 characters, one paragraph; judge found business-like noise and no tells | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The card and design note declare the same family (stump_class analytical; the easy route is arrival-order pairing at GBP 189,330 against 127,785), so there is no mismatch. The declared distractors are not named as the surface read; the thread named none. One mild note: the thread says the daily sheet's backlog "nudges toward a pile". The sheet's bay counts track the running net and corroborate a stack without discriminating the order, so it does not carry the call. Gate G passes.

Gate H line: domain pass, layers pass, decisive_step analytical (borderline).
Borderline note, reconciled: the thread feared newest-first reads as a withheld rule. The design note's "Not rule application" and "No decoy" lines say no filed document states a pairing or picking practice, and the card's analyst_test places the decisive step in testing the arrival-order assumption on labelled openings. The labelled openings make it a measured behaviour, not a rule: 181,318 of 181,318 newest-first against 1,759 arrival order, across 13 months of December 2024 to April 2026 with 2025 reproducing Feb 615 and Dec 889 late refunds. A solver has to run the comparison; no sentence invites it. I accept the design note's reading. The risk is that the step is a one-comparison discovery (stump power moderate: a solver who fits candidates on return_label succeeds). The card text ("2025 and January 2026") understates label coverage, as does CC1; align them.

## Stump power (Gate F)
Moderate, per the thread. The easy route (arrival order, or opening day as delivery) files a wrong, plausible answer. A solver who inspects return_label and tests candidates lands the call. This is the test-and-select organ, not a textbook route with a single obvious method; the main thread weighs it against the design note's ladder.

## Findings, ranked
1. Wording (FIX_NOW): CC1 and step 3 say labelled openings are "2025 and January 2026"; they run to 12 April 2026. Reword in the submission (and card text if it repeats it). No figure moves.
2. Ask 4 fork (optional): the prompt names no order for the category. A one-clause pin narrows it; the asks are free of the main-call rules, so it can stand.
3. Voucher currency inference (informational): forced by redemption evidence.
4. Feb/Mar label gap is an extrapolation of newest-first (informational; no alternative survives).

## Next action for the author
Reword CRITICAL_COMPONENTS 1 and step 3 of submission.md to say the labelled openings run from December 2024 to 12 April 2026, then rerun the free gates (no rebuild); optionally add the order-pinning clause to ask 4.
