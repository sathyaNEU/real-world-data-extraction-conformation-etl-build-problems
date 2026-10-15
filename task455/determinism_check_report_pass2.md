# determinism-check report (pass 2), task455, 2026-10-15

Re-judge after the pass 1 FIX_NOW (architecture 2). One isolated thread, scratch /tmp/determinism-check-task455-20261015102714/.

## Verdict
DETERMINISTIC (no SOLUTION_WRONG).
**Disposition:** APPROVE. The pass 1 forks F1 and F2 are closed by the prompt's new wording. An optional pin for the 2025 births remains (supplementary only).
**Stumping type:** mechanism: etl_conformance / method_selection (successor linkage from worker flows), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Executing the prompt and the filed definitions word for word on the shipped files gives Eskwell, Dunrath, Quarrin. Caldmere is first out at 7.8, 1.7 below Quarrin. The two pass 1 conventions are now closed by the text:
- 2025 births are "counted as 2026's are". The register liability_date (dictionary: date of first payroll) settles which accounts first reported employment in 2025.
- Each county is "where its worksite lies". The dictionary defines the register county_code as the geocoded worksite county. The QCEW county is ZIP-based through 2025Q2, so it is not the worksite county.

Two lower-order residual forks remain (below). Neither moves the main call or a graded 2026 figure.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Accounts whose first month with employment is in 2026 (qcew, register liability_date) | 702 | 702, all with 2026 liability_date | yes |
| Continuations (register predecessor_account; ui_wage_records worker_key) | 56 + 72 = 128 | 56 + 72 = 128 | yes |
| 2026 births, Eskwell/Dunrath/Quarrin/Caldmere/Tolbeck/Brennock/Fennamore | 86, 121, 82, 55, 44, 113, 73 | same | yes |
| Set aside, same order | 12, 14, 8, 29, 27, 23, 15 | same | yes |
| Q4 2025 base (qcew) | 759, 1236, 863, 702, 612, 1618, 1104 (6,894) | same | yes |
| 2026 rates | 11.3, 9.8, 9.5, 7.8, 7.2, 7.0, 6.6 | 11.33, 9.79, 9.50, 7.83, 7.19, 6.98, 6.61 | yes |
| Gap, Caldmere to Quarrin | 1.7 | 1.667 | yes |
| 2025 births (2025 liability date, register county) | 542 | 118, 52, 104, 77, 81, 63, 47 = 542; rates 7.3, 7.4, 8.5, 10.4, 7.3, 7.1, 7.7 on a Q4 2024 base of 6,895 | yes |
| 2025 deaths (last employment month in 2025, none in 2026, no predecessor, not more than half carried to one other account) | 527 | 110, 54, 88, 53, 80, 96, 46 = 527; rates 6.8, 7.7, 7.2, 7.2, 7.2, 10.8, 7.5 | yes |

Orders above follow the judge's county order for the 2025 rows (Eskwell, Dunrath, Quarrin, Caldmere, Tolbeck, Brennock, Fennamore).

Boundary check: of 421 old-new pairs, fewer than 8 fall between 0.3 and 0.8 overlap, so any threshold from 0.5 to 0.8 gives the same 574 births. For deaths no pair lies between 0.4 and 0.8, except ties at 1 of 3 workers.

## Competing answers that survived
Main call: none. Stress tests of alternative readings:
| Variant | Top three | Closed by |
|---|---|---|
| Old-side share over 0.5 (golden) | Eskwell, Dunrath, Quarrin | |
| Old-side, either direction | same (Quarrin 8.8) | call unchanged |
| Register predecessors only (56) | Eskwell, Caldmere, Tolbeck | dictionary (an unfiled takeover has no predecessor) and guideline 3.3 (a business that goes on under a new account) |
| New-side share over 0.5, or both sides | Eskwell, Caldmere, Dunrath | guideline text: a business goes on when its workforce carries over; the reading would also treat a 4-worker start-up staffed from a 147-worker closed payroll as a continuation |

Residual forks (supplementary or sub-rounding only):
- R1. The workforce rule is not filed word for word (old-side, "more than half", "that quarter or the next"). The guideline text and the bimodal data force old-side. A next-quarter-only window gives 581 births (Eskwell 11.6, Caldmere 8.1), the same top three, but unrounded Eskwell and Caldmere figures change. Same-quarter and both-quarter windows reproduce the golden.
- R2. The 2025 births depend on the liability_date filter. 88 accounts with a first payroll before 2025 (dormant, reactivated) first show employment in 2025. A QCEW-only reader gets 630 (register plus wage) or 652 (register only) against the golden 542. The register field definition supports the filter and none of the 702 accounts of 2026 triggers it. Supplementary-answer risk only.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 10 | yes |
| Formats | 3 or more | 4 (csv x5, pdf, xlsx x2, txt) | yes |
| Large file | 25,000 rows or more | wage records 617,928; QCEW 65,426 | yes |
| Distractors in metadata.json, none labelled by file name | 2 or more | 3: population estimates, SOS filings, FY2026 grant disbursements | yes |
| Distractors unused, weighable, ruled out by a shipped fact | yes | judge found none used by any step and none carrying the call | yes |
| Deliverables | 1 to 3, all in golden | 2 (pdf, xlsx), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | per-county, per-year cuts; counts whole, rates to one decimal, per 100 establishments | yes |
| Prompt | one paragraph, under 1,000 characters, no persona | one paragraph, 998 characters | yes (2 under the cap) |
| Prompt shape identifiable; rubric 25 or more criteria | yes | shape 01 (ranked list under a cap); rubric is generated at build and not counted here | shape yes; count not verified |
| Reads as real work product, not LLM generated | yes | no authoring or provenance leakage found; golden memo reads as a bureau memorandum; full golden-realism read not repeated | yes, with that limit |

## Gate G reconciliation
Judge: mechanism etl_conformance / method_selection (successor linkage from worker flows), stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The design note's stump sentence declares the same mechanism. The filed-predecessor route ends on Caldmere, Eskwell, Tolbeck (11.1 and 10.8). The new-side workforce route ends on Caldmere, Dunrath, Eskwell (Caldmere about 10.1). The old-side workforce route ends on Dunrath, Eskwell, Quarrin (Caldmere 7.8, Tolbeck 7.2, Quarrin 9.5). The judge's figures match these. The judge named no declared distractor as the surface read carrying the task, and the distractors are not load-bearing. No shipped artifact ranks the counties wrong. Match: no mismatch, no finding.

## Gate H three-rules line
domain: pass, layers: pass, decisive_step: analytical. This matches the card (`stump_class: analytical`) and the design note's `## Three rules`. Swap test: worker-flow linkage of accounts to establishments is the labour-statistics method for births, so another field's nouns change the task. Layer 1 is the ZIP to geocoded county shift, legacy to new account numbering, NAICS 2017 to 2022 and transfers missing from the register. Layer 2 is the successor-predecessor continuity test from the old account's side, which carries the stump. The judge found no decoy and no semantic or rule-application decisive step.

## Stump power (Gate F)
Good, genuinely hard and not a coin-flip. The easy routes (all new accounts; register predecessors only; new-side or symmetric share) each file a wrong top three, with Caldmere in. A strong analyst who cleans the data and reads the guideline correctly can still fail by taking the easy successor definition. The residual pass 1 caveat, that a reviewer may read the 72 workforce-only continuations as a planted incompleteness, is answered by the dictionary's statement that an unfiled takeover has no predecessor and by guideline 3.3. It is a live-test question, not a determinism one.

## Hygiene
PASS. Layer 1 mess is present and operational. File dates are coherent (extract 2027-05-14, guideline 2027-02-02, Q4 2026 reports due 2027-04-30). Nothing exclusion-level. Row counts moved since pass 1 (wage file 608,789 to 617,928, QCEW 65,564 to 65,426), which is consistent with the rebuild; the metadata rows match the pass 2 count.

## Findings, ranked
1. R2: the 2025 births rest on the liability_date filter, which the prompt does not state. Supplementary only; the dictionary supports it.
2. R1: the window of the workforce rule is not literal in the text. It does not change the top three and the golden is reproduced by the same-quarter and both-quarter windows.
3. Rubric criteria count and a full golden-realism read were not re-verified in this pass.

## Next action for the author
None required. Proceed to ship. If you want the 2025 births closed, add a clause to the prompt that 2025 births exclude accounts whose liability date is before 2025. That files the population, not the method. Do not file the share rule. The prompt is at 998 characters, so a clause would need an offsetting cut.
