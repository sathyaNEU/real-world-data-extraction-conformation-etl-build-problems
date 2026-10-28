# determinism-check report, task118, 2026-10-28

Architecture 4 (the States of Eskerholm's 2027 duty envelope). target.zip sha256 `8031742f5cae45ee31287b77d69b37030559feb63d3c551c0609f9a19d49ea2e` (prefix matches the stated `8031742f5cae45ee`). Fresh unzip for the isolated thread: `/tmp/determinism-check-task118-1793160056/target/`.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The isolated judge thread, seeing only prompt.txt, the twelve shipped files and the five graded blocks, independently refit the AR(1) partial-adjustment demand model per duty on the stacked 2008-2026Q3 clearances/price series, solved the GBP1.5m-envelope excess-burden integral on the whole duty+GST wedge, and reproduced spirits ≈GBP0.88m (rounds to 0.9) and cider ≈GBP0.41m (rounds to 0.4), matching FINAL_RECOMMENDATION and CRITICAL_COMPONENTS exactly, including the "nearly all by Q4" (spirits 99.1%) vs "under a third" (road fuel 19.8%) response-fraction claims. It separately rebuilt the CE14 dedup/correction-chain/cancellation/UTC-to-UK-local logic from `customs_excise_declarations_2025-07_2026-09.csv` cross-checked against `bonded_warehouse_register_2026.xlsx` and got an exact match on all 20 cells of the `budget_2027_duty_envelope.xlsx` supplementary table to the stated GBP-thousand decimal. The one fork the thread tested directly (static vs lagged-adjustment elasticity, which flips the naive pick to road fuel) closes in the data itself: Durbin-Watson on the static residuals shows severe autocorrelation (0.20-0.95, every duty) and the lagged model wins decisively on AIC with p<0.0001 lag coefficients. Gates A-E pass.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Spirits excess burden removed, 2027 | ~GBP0.9m | GBP0.88m (rounds to 0.9) | yes |
| Cider excess burden removed, 2027 | ~GBP0.4m | GBP0.41m (rounds to 0.4) | yes |
| Beer / wine excess burden (context) | "~a quarter of spirits" | GBP0.20m / GBP0.21m | yes |
| Road fuel excess burden (context) | not stated numerically, named "under a third" response | GBP0.15m (lowest), 19.8% of long-run response by Q4 | yes |
| Spirits response fraction by Q4 | "nearly all" | 99.1% of long-run | yes |
| Road fuel response fraction by Q4 | "under a third" | 19.8% of long-run | yes |
| Bonded-warehouse excise by duty x quarter (20 cells) | stated in submission | exact match to GBP-thousand decimal, all 20 cells | yes |
| Static-model winner (naive route) | not claimed, probed by thread | road fuel, naive EB ≈GBP1.95m vs spirits ≈GBP1.11m | consistent with design note's conjunction table |

## Competing answers that survived
None at the DETERMINISTIC-gate level. The thread's own Gate C stress test only exercised the response-horizon fork (static vs lagged-adjustment demand model); it did not independently re-derive whether the manual forces the "whole wedge" marginal-excess-burden valuation (CRITICAL_COMPONENTS #2) over a Harberger-triangle-only valuation of the cut alone. The design note (`DESIGN_NOTE.md`, "The conjunction" and "No hill-climb" lines) states this is a genuine second, independent fork: triangle-only valuation + the lagged model still files cider, not spirits, and only whole-wedge + lagged files spirits. The "whole wedge, not half the cut" rule is the standard marginal-excess-burden convention for a rate change on an already-distorted good (Browning/Harberger), which is the field-correct practice rather than an arbitrary choice, and the design note's "Not rule application" line confirms no filed rule in the manual pins it either way — it is a modelling choice the field's own correct method forces. This is consistent with the shipped method producing the one deterministic answer, but the thread's verdict.md does not show it was stress-tested the same way the static/lagged fork was. Recorded as a finding below; not treated as an open fork because the design note's own economic argument for the whole-wedge convention is sound and the "Not semantics"/"Not rule application" lines in the design note explicitly address it.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | >=10 | 12 | yes |
| Format mix | >=3 | csv, xlsx, pdf, eml (4) | yes |
| Large file | one file >=25,000 rows or large DB | `customs_excise_declarations_2025-07_2026-09.csv`, 80,653 rows | yes |
| Distractors named, not in filenames | >=2 in metadata.json, none labelled by filename | 3 named (`excise_receipts_monthly_cash_2020-2026.csv`, `retail_price_survey_quotes_2026.csv`, `passenger_allowance_declarations_2025-26.csv`); none named "distractor" in filename | yes |
| Distractors relevant, unused, one reproduces arithmetically and is ruled out by a shipped fact | the cash-receipts file plausibly answers the "excise accounted for" ask under a cash/deferred-payment basis and is ruled out by CE14's accrual-at-release rule (`customs_excise_accounting_note_ce14.pdf`); the other two are relevant to the duty/price world but unused | yes |
| Deliverables | 1-3, all present in golden, no required format family | 2 (`budget_2027_duty_cut_paper.docx`, `budget_2027_duty_envelope.xlsx`), both present under `golden/` | yes |
| Asks multi-dimensional, unit/rounding stated | required | main ask (5-duty ranking) and supplementary grid (5 duties x 4 quarters = 20 cells); prompt states "nearest GBP0.1 million" and "GBP thousand to one decimal" explicitly | yes |
| Prompt shape identifiable, rubric >=25 criteria | required | metadata.json `prompt_shape: "07"`; design note records 26 criteria (4 main-call figures + 20 grid cells + 2 file-following); pipeline.json records `"rubric": "PASS"` | yes |
| Nothing LLM-generated, goldens read as real work product | required | thread found no provenance/benchmark-disclosure/LLM-authorship tells in the eml, PDFs or CSVs; dates and fictional timeline internally consistent | yes |

## Gate G reconciliation
Thread: `mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
Card (`.claude/skills/fingerprint/cards/task118.json`): `gate_g: method_or_model_selection`, `stump_class: analytical`.
Design note `## Three rules`: Layer 2 `field_method`, decisive step named as "valuing each duty's cut on the whole wedge... over the response made by each quarter of 2027 from the fitted lagged adjustment, the conjunction of two moves each of which alone files a different wrong duty."

These align: no mismatch on mechanism or family. The thread did not name either declared distractor as carrying the surface read (it correctly identified all three as unused and relevant, consistent with "No decoy" in the design note). The one gap is noted above: the thread's stress test closed only the response-horizon axis (G13) of the design note's two-axis conjunction, not the valuation-method axis (G1, whole wedge vs the cut's own triangle), even though both are needed to land on spirits. Because the valuation convention is the field's standard marginal-excess-burden practice (not an arbitrary or filed rule, matching the design note's "Not rule application" line and the determinism-check skill's allowance for a standard's general method to force a step), this does not change the DETERMINISTIC verdict, but it is the one piece of the judge's own verification that is less complete than the rest of an otherwise thorough recomputation.

## Stump power (Gate F)
The thread's Gate F read is sound: a strong model that fits a simple static log-log elasticity (no lag term, no residual-autocorrelation check) will credit road fuel with its full long-run elasticity as if achieved within the single Budget year, and will recommend cutting road fuel duty — a specific, provable econometric error (treating long-run response as within-year response), not a coin flip. The design note's own measured conjunction table confirms a second, independent trap: valuing the cut only by its own Harberger triangle (ignoring the pre-existing wedge) lands on cider even with the correct lagged model. Both traps are genuine method-selection errors on honest data (no planted defect, no misleading reported number), landing squarely in the FINE-numbers method_or_model_selection shape the client wants. This is a legitimate, well-targeted two-axis conjunction stump, matching the design note's intent ("no hill-climb").

## Findings, ranked
1. (Low severity, no disposition change) The judge thread's Gate C stress test verified only one of the design note's two independent forks (static-vs-lagged response horizon) and accepted the "whole wedge, not half the cut" valuation convention from CRITICAL_COMPONENTS #2 without independently re-deriving that it is the field-forced choice rather than a defensible triangle-only alternative. The design note's own economic argument (the standard marginal-excess-burden formula for a rate cut on an already-distorted good) supports forcedness, and "Not rule application" in the design note explicitly addresses this, so no SEND_BACK is warranted; noting for the record that a future repeat review on this task should explicitly stress-test the valuation-method fork the same way the response-horizon fork was tested.
2. (Informational) `DESIGN_NOTE.md`'s append-only `## Tried and rejected` history still carries extensive material from architectures 1-3 (a media/publishing "desks and headlines" domain), which is expected and compliant with the "append-only, kept as history" rule for design notes, not a defect of architecture 4's build.

## Next action for the author
None required to ship architecture 4: APPROVE and proceed. If a future repeat review of this task (or a near-neighbor re-draw) is run, have the judge thread explicitly stress-test the whole-wedge-vs-triangle valuation fork (not only the static-vs-lagged response fork) against the shipped files, to fully close the design note's stated two-axis conjunction.
