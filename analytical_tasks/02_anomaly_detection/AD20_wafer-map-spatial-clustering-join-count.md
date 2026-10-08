# AD20 — Wafer excursions: a scratch with five bad dies matters more than a wafer with fifty random ones

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Semiconductor yield engineering at foundries and device makers (spotting systematic defect signatures that point to a tool or process step) |
| Domain | Semiconductor manufacturing |
| Task shape | 07 · Grid of cells (labelled pattern class × detection rule → detection rate; adopt the rule meeting the memo's criteria) |
| Core method | Spatial autocorrelation of failing dies: join-count statistic (fail–fail adjacencies) against its expectation under spatial randomness at the wafer's own fail rate; z-score flag for systematic patterns |
| Analytical stump | Yield (or fail count) thresholds flag wafers with many random fails and miss low-count systematic signatures (scratches, edge-local, center) that indicate tool problems. Clustering must be tested conditional on the wafer's own fail rate |
| Primary sources | WM-811K wafer map dataset (MIR lab, Wu et al., IEEE TSM 2015) |

## 1. The real-world situation

A fab's yield team triggers an engineering review when a wafer shows a **systematic** failure pattern, because systematic patterns trace
back to a specific tool or step. The current trigger — wafer yield below 80% — sends dozens of randomly defective wafers for review and
misses scratches and edge-local patterns on otherwise high-yield wafers.

## 2. The decision (one deterministic recommendation)

**Adopt the join-count trigger or keep the yield trigger, judged on detection of systematic classes and the false-trigger rate on
"Random" and "none" wafers.**

Rules (yield engineering memo):

* Wafers: labelled wafers in WM-811K; dies with value 2 = fail, 1 = pass, 0 = off-wafer.
* Yield trigger Y: fail fraction ≥ 0.20.
* Join-count trigger J: with n die on the wafer and fail fraction p, observed fail–fail rook adjacencies BB; expected E[BB] and variance
  under random labelling (formulas in the memo, using the wafer's adjacency counts); z = (BB − E) ÷ √Var; trigger if z ≥ 3 and at least 5
  failing dies.
* Systematic classes: Center, Donut, Edge-Loc, Edge-Ring, Loc, Scratch, Near-full; non-systematic: Random, none.
* Adopt J if its detection rate is higher than Y's for at least 5 of 7 systematic classes and its trigger rate on non-systematic wafers is
  ≤ 5%.

## 3. Why capable analysts get it wrong

* Yield is the headline metric; low yield feels like the anomaly.
* Random defects at high density are a different problem (contamination, wafer-level) than localized patterns (tools).
* Clustering tests must condition on the fail rate; raw adjacency counts grow with p.
* Edge effects (fewer neighbours at the boundary) must be handled through the wafer's own adjacency structure.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `LSWMD.pkl` | Pickle (pandas) | 811,457 wafer maps | WM-811K (MIR lab; widely mirrored) | Public research dataset (verify terms) | Wafer maps, labels, lot IDs |
| 2 | `wafer_maps_labelled.npz` | NumPy | ~172k | Derived | Same | Labelled subset |
| 3 | `wafer_features.parquet` | Parquet | ~172k | Derived | Same | n, p, BB, E, Var, z |
| 4 | `wu_2015_tsm.pdf` (citation) | PDF | — | IEEE TSM 2015 (cite) | Cite | Dataset description |
| 5 | `join_count_statistics_reference.pdf` (citation) | PDF | — | Cliff & Ord (cite) | Cite | Join-count formulas |
| 6 | `yield_engineering_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `current_trigger_log.xlsx` | XLSX | ~100 | Task author | — | Yield-trigger outcomes |
| 8 | `failure_type_counts.csv` | CSV | 9 | Derived | Same | Class sizes |
| 9 | `adjacency_reference_cases.json` | JSON | — | Task author | — | Small test maps for verifying formulas |
| 10 | `lot_level_summary.csv` | CSV | ~46k | Derived | Same | Context |

## 5. Deterministic solution path

1. Parse maps; compute n, p, rook adjacency counts and BB per wafer.
2. Compute E, Var, z under random labelling; apply J and Y.
3. Detection rates per class; non-systematic trigger rates; decision.

## 6. Wrong paths (method errors, not misreadings)

**A — yield trigger.** Misses Scratch/Edge-Loc/Loc; triggers on Random.

**B — raw BB threshold.** Confounded with p.

**C — ignoring edge structure.** Biased expectations.

**D — evaluating on unlabelled wafers.** No ground truth.

## 7. Why the stump is analytical, not semantic

Labels and formulas are given. The trap is confusing level (fail rate) with structure (spatial clustering).

## 8. Draft task prompt (prose)

> Should we switch our wafer review trigger from yield to the spatial-clustering test in the yield engineering memo? Evaluate both on the
> labelled WM-811K wafers and give me adopt or keep. Provide `trigger_grid.csv` (class × trigger: wafers, detection rate), `example_maps.png`
> (one wafer per class with its z-score and fail fraction), and a one-page `trigger_decision.pdf`.

## 9. Deliverables

* `trigger_grid.csv`, `example_maps.png`, `trigger_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 9 classes × 2 triggers = 18 rates; non-systematic trigger rates; decision; reference-case checks.

## 11. Golden-output checklist

* Correct die coding; rook adjacency; E/Var formulas; thresholds; class evaluation; decision.

## 12. Build notes (scope tuning)

* Verify the label encoding in the pickle (nested arrays) and document cleaning.
* Confirm J beats Y on most systematic classes while keeping non-systematic triggers low.
