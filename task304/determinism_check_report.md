# determinism-check report, task304, 2026-10-27

## Verdict
**DETERMINISTIC**
**Disposition:** APPROVE, no repair needed, no rerun required.
**Stumping type:** mechanism: method_or_model_selection (borderline against single_conceptual_flip), stumping_family: analytical_non_defect (borderline), surface_read_dependency: no (borderline, see caveat), sole_data_defect: no

## Why
This is the one re-judge licensed for a FIX_NOW: the prior pass (reproduced above the fold in this folder's history) found a false superlative in the committed recommendation text ("a quarter of arrivals test antibody positive, the highest share of the four", false, needle exchange registrants were highest at ~38%) and sent it to FIX_NOW. That sentence is gone from the current `submission.md`: the Final Recommendation now states only "a quarter of arrivals test antibody positive" for approved premises, with no superlative claim, and the main call, the stump, and every graded figure are otherwise frozen per the fix command's contract.

The isolated judge thread (fresh unzip of `target.zip` at `/tmp/determinism-check-task304-1793152872/target/`, 12 files, the extracted submission blocks, nothing else) independently rebuilt every committed figure from the shipped files rather than trusting the solution blocks, and all of them reproduced exactly: the four settings' found/started figures (AP 10/10, HH 30/20, DS 40/30, NSP 70/50) and all ten cells of `van_2027_funnel.xlsx`. The decisive fact, that an antibody-reactive arrival is not necessarily an active infection, because antibodies persist after a cure recorded in a different organisation's system (Corvane Health's prison courses or the network's own register), is fully present and locatable in the shipped files (`fenwold_hcv_pathway_2026.pdf` §3, `corvane_hcv_courses_2017-2026.xlsx`, `hcv_treatment_register_2015-2026.csv`). Gates A–E all pass; the main recommendation (needle exchange registrants, ~50 starts vs. Fenwold Recovery's ~30) is forced.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Van tested 0.65, started 0.74 of RNA-detected within 12 weeks | 937/1450=0.65, 160/215=0.74 | 0.6462 / 0.7442 | Yes |
| Two-year averaged arrivals (AP/HH/DS/NSP) | implicit in step pipeline | 1001 / 1005 / 2061 / 493.5 | Yes |
| Reactive share by setting | implicit | AP 0.251, HH 0.161, DS 0.146, NSP 0.386 | Yes |
| AP positives cured inside prison before arrival ("more than half") | >50% | 355/406 total cured = 87% (direction and magnitude both support "more than half") | Yes |
| Found/started, all four settings, after round-to-nearest-ten | AP 10/10, HH 30/20, DS 40/30, NSP 70/50 | AP 8.9→10/6.6→10, HH 30.9→30/23.0→20, DS 38.6→40/28.7→30, NSP 71.4→70/53.1→50 | Yes, all eight cells |
| Funnel xlsx, all 10 cells (5 clinics × 2 half-years) | HEP 15/11, COMM 9/26, FRC 43/33, PHARM 3/11, OUT 30/55 | rebuilt the cure rule from `fenwold_hcv_pathway_2026.pdf` (Completed vs Stopped vs Lost-to-follow-up last-dose handling) plus cross-pseudonym `lims_patient_id` linkage: identical on all 10 cells | Yes |
| False superlative ("AP highest antibody-reactive share") flagged in the prior pass |, | absent from current submission.md; not reasserted anywhere in the current blocks | Fixed, confirmed absent |

## Competing answers that survived
None. The judge enumerated the naive proportional-count answer (ignore all cure records; the largest raw intake, Fenwold Recovery's new entrants, wins) as the trap the task is built to catch, not a surviving defensible alternative, a shipped fact (the cross-system cure records) rules it out. The NSP–DS margin (24 people unrounded, 20 after rounding) sits well outside anything the tested sensitivities (match-window choice, the no-prior-record default share) can close; the 60-day peer-test matching window is forced by a natural gap in the arrival-to-test date-diff histogram, not an arbitrary author pin.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | ≥10 | 12 | Pass |
| Format mix | ≥3 formats | csv (7), pdf (3), xlsx (2) | Pass |
| Large file | ≥25,000 rows or large DB | `virology_hcv_results_2015-01_to_2026-09.csv`, 238,968 rows | Pass |
| Distractors named, not filename-labelled | ≥2 in metadata.json, none named "distractor" in a filename | `nsp_pharmacy_transactions_2025-04_to_2026-09.csv`, `fibroscan_sessions_2025-26.xlsx`; neither filename says "distractor" | Pass |
| Distractors relevant and unused | each weighed, unused | nsp_pharmacy is explicitly weighed in the design note's fork table (SF22: an alternate source for needle-exchange arrivals, "same call" either way, plausible and unused); fibroscan is clinically adjacent (liver-scan sessions) but is not discussed anywhere in the design note's fork table | Partial, fibroscan's "relevant enough to weigh" case rests only on topical adjacency, not a demonstrated near-miss computation; not a blocking gap given disposition APPROVE |
| Deliverables | 1–3, all in golden | 2 (`van_2027_trustee_paper.docx`, `van_2027_funnel.xlsx`), both present in `golden/` | Pass |
| Asks multi-dimensional, unit+rounding stated |, | 4 settings × 2 metrics, 5 clinics × 2 half-years; "Round people to the nearest ten and give cures as whole counts" stated once in the prompt, governs all asks | Pass |
| Prompt shape identifiable, rubric ≥25 criteria |, | shape "09" per the fingerprint card; no rubric artifact is checked into the task folder to count criteria directly (generated at grading time via `generator/cracker.py`'s ask/mirror criteria machinery) | Not independently verifiable from this folder; no evidence of a shortfall |
| Nothing LLM-generated, goldens real-product |, | judge's hygiene check: PASS, no README/benchmark/synthetic disclosure anywhere (grepped across all 12 files); dates internally coherent | Pass |

## Gate G reconciliation
The thread landed on `method_or_model_selection` / `analytical_non_defect`, flagged explicitly as borderline against `single_conceptual_flip` (the naive-proxy-metric-vs-needed-metric shape structurally resembles it), but reasoned that no shipped file *reports* a stated "active caseload" number the solver must catch as wrong, the solver builds the figure from nothing, so there is no reported/surface read being rejected. The card's own `gate_g` field says `forecasting` (reflecting the design's intent: the call is about calendar 2027, a window not yet closed, sized from pilot rates carried forward). These are different labels but both are non-banned FINE-numbers shapes; neither the thread nor the card names a surface-read-rejection, so there is no mismatch of the disposition-changing kind.

One genuine divergence worth recording: the thread's named "easy route" for stump power (a model that computes active caseload as roughly proportional to raw antibody-reactive counts, landing on Fenwold Recovery's new entrants, the largest raw intake) is a *cruder* error than the design's own `analyst_test` on the card and in the design note, which describes a *near-thorough* analyst who does cross-reference the network register and Fenwold Pathology for cures but misses only Corvane's prison workbook specifically, landing on **approved premises** at about 80 starts, not Fenwold Recovery. The thread verified the crude all-cures-ignored naive path numerically but did not separately verify the sharper, intended near-miss path (register+pathology cross-check, prison workbook omitted) that the design note treats as the actual decisive trap. Both easy routes are still `H3: analytical` (the missing step is a cross-system join in either case) and neither changes the DETERMINISTIC/APPROVE call, since the thread did independently confirm the golden figures and the AP/DS/NSP/HH figures all reproduce under the full correct method. But the author should confirm in live testing that it is the design's sharper trap (a solver who did real cross-referencing against the network register and Pathology, and still lands on approved premises for missing only the prison-specific workbook) that is doing the stumping, not just the cruder no-cure-screening-at-all error, the latter is a much easier mistake to avoid and would overstate stump power if it is the only failure mode the author checks for.

## Stump power (Gate F)
The thread's assessment: the trap is real and would catch a model that treats "active caseload" as proportional to raw antibody-reactive counts, since Fenwold Recovery's new entrants then wins on raw intake size alone. Per the reconciliation above, the design's own intended trap is sharper still (a model that does the right cross-system work against the network register and Fenwold Pathology, but never discovers that Corvane Health's prison workbook is a third, necessary source, and lands on approved premises instead), this is the library's standard HCV case-finding method applied with no judgment call the data had to settle (an `analytical`, textbook-method route per `stumping` 1.3), which is a landable call for a strong solver and should be weighed by the author against the design note's ladder as the primary evidence of difficulty, not the cruder proportional-count error the thread verified first.

## Findings, ranked
1. (Informational, not blocking) The thread's Gate G/H stump-power narrative verified the crude "ignore all cure records" naive route rather than the design's own sharper intended near-miss ("cross-reference register+Pathology, miss only Corvane's prison workbook"), both are `H3: analytical`, but the author should confirm live model failures track the intended sharper trap, since that is the stronger evidence for stump power.
2. (Informational, not blocking) `fibroscan_sessions_2025-26.xlsx`'s case as a "relevant enough to weigh" distractor rests on topical adjacency alone; the design note's fork table discusses `nsp_pharmacy_transactions...csv` explicitly (SF22) but never discusses fibroscan.
3. No Gate A–E, Gate G, or Gate H failure. The prior pass's false-superlative defect (FIX_NOW) is confirmed fixed and not reasserted anywhere in the current submission blocks.

## Next action for the author
None required, ship as-is. If stump-power evidence from live testing looks weaker than expected, check whether models are failing via the crude proportional-count route (easy to avoid) rather than the intended register+Pathology-but-not-Corvane near-miss (the real test of the task); if models are clearing the task by only doing partial cross-referencing, consider the design note's own fork table (SF22 and the "standing family" paragraph) as the place to look before touching the prompt or data.
