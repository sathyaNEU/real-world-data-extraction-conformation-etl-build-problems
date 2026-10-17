# determinism-check report, task264, 2026-10-17

## Verdict
DETERMINISTIC (main call and workbook asks reproduce; three supplement-side wording forks open)
**Disposition:** FIX_NOW
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judge thread: one pass, general-purpose, sonnet, medium, scratch prefix /tmp/determinism-check-task264-064639/ (verdict at verdict.md there).

## Why
Executed literally, the methodology (matched-model GEKS-Tornqvist per format, first-four to last-four weeks, committee Table 1 weights, 1.5-point test) gives 10 categories. The widest published gap is 1.09 (Yoghurt, online) and the nearest excluded misses at 2.30 (Fresh meat and poultry, neighbourhood), so the margin is clean. The pricing unit (a line at its chain) is forced by partner_chains.xlsx (one shelf price per line across a chain's stores), the feed dictionary (a store that sold none has no row) and methodology section 1. Wrong routes: store-by-store matching gives 7, format averaging gives 4, format averaging without S5 gives 8.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Categories published | 10 | 10 | yes |
| Widest published gap | 1.1 (Yoghurt, online) | 1.09 | yes |
| Nearest excluded | 2.3 (Fresh meat, neighbourhood) | 2.30 | yes |
| Convenience gaps (Cereals, Cheese, Deli, Biscuits) | -0.2, -0.8, -0.6, -0.5 | -0.22, -0.82, -0.56, -0.47 | yes |
| Coffee and tea convenience gap | 2.4 | 2.38 | yes |
| 18 national changes and 72 gaps | ask 2 | reproduced from unrounded changes | yes (see fork F1) |
| 18 promotion shares | ask 3 | reproduced with C2 PC as special before 8 Aug 2026 | yes (see fork F2) |
| Sales by format A$m | 804.4 / 230.7 / 86.7 / 466.6 | 804.389 / 230.728 / 86.679 / 466.594 | yes |
| Continuity counts, 14 chains | ask 5 | reproduced exactly | yes (see fork F3) |
| Alternatives 7 / 4 / 8 | stated | 7 / 4 / 8; chain-line without S5 still 10 | yes |

## Competing answers that survived
- F1 Gap rounding (ask 2, gpi_2027_structure.xlsx): golden gaps use unrounded changes. Subtracting the rounded one-decimal changes moves many digits (Bread supermarket 0.0 becomes 0.1, Eggs neighbourhood -0.1 becomes -0.2). Prompt does not say which basis. Classification unaffected. Design note row 10 (rounding path) claims "prompt" closes it; the prompt does not.
- F2 C2 "PC" code (ask 3): the dictionary says a price check is not a promotion. Literal reading: C2 PC is never a special, shares fall 0.2 to 0.6 points (Biscuits 13.1 vs 13.7), most of 18 values change. Golden reading (PC is a special before C2's first TPR week, 8 Aug 2026) is inferred from the code list dated 3 Aug 2026 and the log note, never stated. Third reading (PC a promotion throughout) differs only at Cheese (14.3).
- F3 Store continuity (ask 5): "every week it was in the panel" read as the chain's panel weeks (golden, C1 12) or each store's own period (C1 13, C2 17). Syntax points to the chain, but the sales ask says "while they were in the panel" for stores.
- F4 Store-week total rows (ask 4): C3, N2, O3, S3 repeat the store total on both department rows; counted once by inference, no stated rule (design note referee: "no file says which chains repeat the store total"). Judge reproduced it, but a literal sum double counts those chains. Open unless the files signal it; note only.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | yes |
| Formats | 3 or more | csv, xlsx, pdf | yes |
| Large file | 25,000 rows or more | gpi_movement_ry2026.csv 726,756 rows | yes |
| Distractors | 2 or more in metadata.json, none named by file | household_panel_category_spend_2026.xlsx, shelf_price_audit_2025.csv; names do not label them | yes |
| Distractor unused yet weighable | arithmetic plus shipped fact rules out | judge did not use either; neither named as the surface read carrying the task | yes (not independently tested by me beyond the judge's report) |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, docx), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | all five asks state unit and rounding; asks 2, 3 and 5 are multi-row | yes |
| Prompt shape and 25 criteria | identifiable, 25 or more | shape identifiable (structure plus per-category grid); rubric not generated yet, count not verifiable | not checked |
| Reads as real, not LLM | | judge hygiene PASS; mixed codes, re-codes, rejected resend, Monday-Sunday week present | yes |

## Gate G reconciliation
Judge: method_or_model_selection, analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note: estimation_fit family, stump_class analytical on the card; decisive step is the pricing unit (item at its chain). Card mechanism field is empty (None), so there is nothing to mismatch; the judge's label and the note's Layer 2 agree. The declared distractors are not the surface read carrying the task. Decoy-free: no published figure to reproduce. No mismatch.

## Stump power (Gate F)
Good. Both easy routes file a wrong count (store match 7, format average 4). Margin 1.1 against 2.3 against the 1.5 band is well separated. Asks add independent stumps (sales total rows, store re-coding, PC code).

## Gate H (three rules)
domain: pass, layers: pass, decisive_step: analytical. Layer 1: superseded and rejected loads, 13-digit GTINs, Monday-Sunday chain, store re-codes, till-release code change. Layer 2: matched-model price index built at the unit that sets the price. Easy route: store-line matching (7) or format averaging (4). One caution to the author: the pricing unit is filed only in partner_chains.xlsx and the dictionary, not named by the methodology; the judge accepted it as forced, so no send-back.

## Findings, ranked
1. F2, ask 3 (gpi_2027_structure.xlsx item 3 and prompt.txt "share of its spending sold on promotion"): C2 PC meaning unfiled; 18 values depend on it. Source of truth: partner_chains.xlsx C2 code list (3 Aug 2026), feed_delivery_log note.
2. F1, ask 2 (prompt.txt "gaps in percentage points to one decimal"): rounding basis unpinned; design note row 10 says the prompt pins it and it does not.
3. F3, ask 5 (prompt.txt "in every week it was in the panel"): referent of "it" fork.
4. F4, ask 4 (store_weekly_sales_ry2026.csv): repeat total rows inferred only.
No finding on the main call, files, hygiene or leakage.

## Next action for the author
One generator-side pass: pin in prompt.txt (866 characters now, limit 1,000) that gaps come from unrounded changes and that "in every week the chain was in the panel" is the continuity window; close F2 by a shipped fact (for example a dated line in the C2 entry of partner_chains.xlsx or the delivery log saying PC was the catalogue-special code until the till release) or a prompt pin, and decide F4 the same way; rebuild twice, re-run checks.py and figures_check.py, then re-judge once. No stump or main-call change.
