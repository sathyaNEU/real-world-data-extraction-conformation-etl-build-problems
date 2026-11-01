# determinism-check report, task447, pass 5, 2026-11-01

## Verdict
DETERMINISTIC on the final cut (target.zip md5 02e9335058bbd8a9d816bbbef030e481), after one FIX_NOW applied to the judged cut (cdfe56c7).
The thread judged cdfe56c7: NOT_DETERMINISTIC on one cell only (Exhibit 1, Kinnickinnic gastroenterology, 219); the main call and the other 26 graded figures were forced and reproduced.
**Disposition:** APPROVE on 02e93350, subject to the cell re-check below (done by me, it reproduces). The re-judge of the one changed sentence was not a second thread; I recomputed the cell myself, per the main thread's instruction.
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
- Thread (cdfe56c7): Brightwater baseline 610,000 and referred part 1,600,000 reproduce (total 2,209,205, 2.2 against 2.0M, proceed). The decisive step is the tier-conditioned referral share: 86% where the acquirer is tier 1 or untiered in the projection year, 0% in tier 2, with Bayfield tier 1 from 2025. Margin: any share from 82.8% to 88.2% keeps 2.2.
- The only fork was NPI 1451989697 (Clayton Brown, GI), open-ended under Brightwater (39-9943822) and Kinnickinnic Physician Network (39-1059486, from 2023). Readings gave 219 (claim-level TIN), 520 (history), 311 (dates billed under Kinnickinnic), 174 (Brown out). No sentence chose.
- Fix applied: appendix A2 now ends "A visit counts for the system or the practice under whose taxpayer identification numbers its claim was billed."

## Ruling on the applied sentence
It closes the cell as a WHAT. It files the attribution unit (the visit, by the TIN its claim was billed under), which is a population definition, not a procedure. It excludes the history reading (520, which attributes by the physician's open spans, not the claim), the date reading (311, which attributes by days not by claim) and, with A4's "a physician billing under several of the system's numbers is counted once" and A2's "one of the group's physicians", leaves Brown in for his claims under Kinnickinnic TINs (so 174 is out). It does not file the person linkage across member keys (A2/A3 still say only "each person is one patient"), so the exhibit ask's silent device stays unstated and the ask is not turned into rule application beyond what it already was. It also does not file the HOW of the decisive step of the main call (nothing about tiers). Ruled closed.

## Recomputation ledger
| Figure | Claimed | Recomputed | Reproduced |
|---|---|---|---|
| Brightwater repricing (thread, cdfe56c7) | 610,000 | 609,632.63 | yes |
| Referred services (thread) | 1,600,000 | 1,599,572 | yes |
| Total (thread) | 2.2M vs 2.0M | 2,209,205 | yes |
| Ledgestone PC/GI/ortho/cardiology (thread) | 2,432/57/133/117 | same | yes |
| Kinnickinnic PC / ortho / cardiology (thread) | 5,967/422/306 | same | yes |
| Five practice totals in Exhibit 1 (thread) | 1,716/1,751/539/3,140/1,597 | same | yes |
| Exhibit 2, all 8 cells (thread) | 171/164/59+865/266/742+234 | same | yes |
| Kinnickinnic GI, on 02e93350 (me) | 219 | 219 | yes |

Cell recompute on 02e93350: Kinnickinnic TINs 39-1059486 and 39-3206081 (register); GI physicians by carrier-file taxonomy 207RG0100X (3 NPIs: 1451989697, 1769078498, 1896215476); office visits 99202 to 99215, not POS 10 and not modifier 95, latest version net of replacements, service facility ZIP in the two counties, residence by the eligibility span covering the date, claim billed under a Kinnickinnic TIN: 234 visit lines (49, 96, 89), 228 distinct member keys, 219 persons after merging second-carrier keys (same date and code, same birth year, sex and ZIP, one claim's allowed equal to the other's member liability). Reproduced. (My check of voids found only replacement codes 7 in the claims file.)

## Competing answers that survived
None found on the final cut. The three rival Kinnickinnic GI readings (520, 311, 174) are each ruled out by the new A2 sentence with A4. Residual point, not a fork: the person-merge (second-carrier keys) is unstated by design and is discoverable from the data (thread rated it forced for a rigorous solver; looser tests move cells by 1 to 4).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 17 | yes |
| Formats | 3+ | 4 (csv, json, pdf, xlsx) | yes |
| Large file | 25,000+ rows | 103,388 (eligibility), 73,100 professional | yes |
| Distractors | 2+ in metadata.json, none named by file | HCRIS extract and Medicare Advantage facility claims; file names do not label them | yes |
| Distractor relevant, unused, not an answer | yes | both outside the commercial estimand; thread found the MA file excluded by 4.02(b) | yes |
| Deliverables | 1 to 3 | 1 (N25-014_preliminary_review.pdf), all answers in golden | yes |
| Asks multi-dimensional, unit and rounding stated | yes | whole patients, one decimal, grid of cells | yes |
| Prompt shape, 25+ criteria | yes | shape 07 grid; 2 call figures plus 27 graded exhibit cells | yes |
| Prompt form | one paragraph, under 1,000 chars | 929 chars, no persona or bullets | yes |
| Reads as real work product | yes | thread: no authoring leakage; mild tell, Exhibit C rates uniform multiples of a base schedule | yes (note) |

## Gate G reconciliation
Thread: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note (line 217) and card: the same trio; card stump_strategy composition_mix. Match. The declared distractors (HCRIS, MA claims) are not the surface read carrying the task; the thread named the product-own-history and pooled shares as the easy routes, both from the real Bayfield history (shipped fact, not a planted record). No Gate G finding. (The card has no mechanism field; the note carries it.)

Gate H: thread says domain pass, layers pass, decisive_step analytical. Card stump_class analytical, with analyst_test and domain_test present; the note's Three rules (No decoy, Not semantics, Not rule application) are consistent. Match. The thread's caution stands: the filed phrase "as the product stands in the projection year" (4.04/4.05) is a strong nudge that the most careful solvers may clear.

## Stump power (Gate F)
Moderate to good, as the thread rated it. The trap is the tier-conditioned share: product-own history gives about 1.64M and pooled about 1.48M, both closing; the 2026 tier standing gives 2.2M and proceeds. The thread notes the method is the field's capture model moderated by benefit design and the rule files the estimand's unit, so a strong solver who reads "stands in the projection year" closely can land it (stumping 1.3: a textbook route). The exhibit ask layer adds count precision (key merge, A5 join dates, TIN history). Main thread to weigh against the note's ladder.

## Findings, ranked
1. Resolved: Kinnickinnic GI 219 fork (A2 sentence added); verified.
2. Residual, accepted: person linkage across member keys is unfiled by design; looser tests move 1 to 4 per cell.
3. Minor: "each of those practices" in Exhibit 2 could be stretched to the two systems; harmless to a response listing more.
4. Minor: Exhibit C rates uniform multiples of a base schedule.
5. The report did not re-judge the whole bundle on 02e93350; the main thread states no other file the call reads changed. The thread's other evidence is from cdfe56c7.

## Next action for the author
Ship on 02e93350 with the A2 sentence; no other change needed.
