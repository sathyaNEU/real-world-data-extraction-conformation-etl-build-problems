# FC14 — Releasing a battery lot after 100 cycles: capacity barely moves before the knee

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Consumer-device and EV battery qualification (early screening of cell lots before field degradation; battery-health throttling controversies) |
| Domain | Battery manufacturing / quality engineering |
| Task shape | 10 · Scorecard against thresholds (cell × predicted-life test → lot go/no-go) |
| Core method | Early-cycle feature model (variance of the discharge-capacity difference curve ΔQ₁₀₀₋₁₀(V)) fitted on a training batch, applied to a new batch; lot decision from predicted failures |
| Analytical stump | Capacity fade is nearly flat for the first hundreds of cycles and then accelerates (the "knee"). Extrapolating early fade linearly predicts very long lives and passes every lot; information about future fade is in the shape change of the voltage curve, not in the capacity level |
| Primary sources | Severson et al. (2019) fast-charging LFP/graphite cell dataset (data.matr.io) |

## 1. The real-world situation

A device maker qualifies battery cell lots with an accelerated cycling test but cannot wait for cells to wear out. The rule:
release a lot if no more than 10% of tested cells are predicted to reach end of life (80% of nominal capacity) before **600
cycles**, using only the first 100 cycles. The test engineer fitted a straight line to each cell's discharge capacity over
cycles 2–100 and extrapolated to the 80% line; every cell was predicted to last thousands of cycles, and the lot passed. Field
returns told a different story.

## 2. The decision (one deterministic recommendation)

**Release or hold the new lot (the 2018 batch), and how many of its cells are predicted to fail before 600 cycles?**

Rules (qualification memo):

* Cells and splits as published: training = the paper's training cells (batches 2017-05-12 and 2017-06-30 subset); evaluation
  lot = the 2018-04-12 batch ("secondary test").
* Feature: x = log₁₀(var(ΔQ₁₀₀₋₁₀(V))), the variance over the voltage grid of the difference between the discharge Q(V) curves of
  cycle 100 and cycle 10 (interpolated to the common voltage grid supplied).
* Model: log₁₀(cycle life) = a + b·x, fitted by OLS on the training cells (observed cycle life to 80% of nominal 1.1 Ah).
* Prediction for each lot cell from its own first 100 cycles; predicted failure if predicted cycle life < 600.
* Hold the lot if predicted failures > 10% of lot cells.

## 3. Why capable analysts get it wrong

* Early capacity data look like a gentle linear decline; linear extrapolation is intuitive and wrong for nonlinear degradation.
* Cycle-100 capacity and internal resistance correlate weakly with eventual life; the voltage-curve shape change carries the
  signal.
* Fitting on all cells (including the lot) leaks the answer and overstates accuracy.
* Mixing up the end-of-life definition (80% of nominal vs of initial capacity) shifts lives.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–3 | `2017-05-12_batchdata.mat`, `2017-06-30_batchdata.mat`, `2018-04-12_batchdata.mat` | MAT (HDF5) | per-cycle curves (~1,000 V points × cycles × cells) | data.matr.io (Toyota Research Institute / Stanford / MIT) | CC BY 4.0 (verify) | Raw cycling data |
| 4 | `cycle_summary_all_cells.csv` | CSV | ~100k cell-cycles | Derived | Same | Per-cycle capacity, IR, temperature |
| 5 | `qv_curves_cycles_10_100.parquet` | Parquet | ~250k | Derived | Same | Interpolated Q(V) for cycles 10 and 100 |
| 6 | `cell_metadata.json` | JSON | 124 | Derived from paper SI | Same | Charging protocol, batch, split |
| 7 | `severson_2019_nature_energy.pdf` (citation) + SI | PDF | — | Nature Energy 2019 (cite) | Cite | Feature definition, splits |
| 8 | `voltage_grid.csv` | CSV | 1,000 | Task author (from paper) | — | Common grid |
| 9 | `qualification_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 10 | `engineer_linear_extrapolation.xlsx` | XLSX | ~45 | Task author | — | The flawed predictions |

## 5. Deterministic solution path

1. For each cell, interpolate discharge Q(V) at cycles 10 and 100 onto the grid; compute ΔQ and its variance; x.
2. Fit OLS on training cells; report a, b, training RMSE.
3. Predict lot cells; count predicted failures (< 600); decide.
4. Contrast with linear capacity extrapolation and with a model fitted on all cells.

## 6. Wrong paths (method errors, not misreadings)

**A — linear fade extrapolation.** All cells "pass"; lot released.

**B — capacity/IR at cycle 100 as predictor.** Weak model; borderline decisions random.

**C — fit including the lot.** Leakage; optimistic and different coefficients.

**D — wrong EOL definition.** Lives shift; failure count changes.

## 7. Why the stump is analytical, not semantic

The feature, model, split and threshold are explicit. The error is assuming degradation that is flat early will stay linear —
a modelling error about nonlinear processes.

## 8. Draft task prompt (prose)

> Decide whether to release the new battery lot using only its first 100 cycles, following the qualification memo: predict each
> cell's cycle life with the early-cycle model trained on the earlier batches and hold the lot if more than 10% of cells are
> predicted to fail before 600 cycles. Provide `lot_predictions.csv` (cell: feature, predicted life, observed life where known,
> pass/fail), `capacity_fade_knee.png` showing capacity versus cycle for six lot cells with the engineer's linear extrapolations
> and the model's predicted end-of-life, and a one-page `lot_release.pdf` with the decision and the count of predicted failures.

## 9. Deliverables

* `lot_predictions.csv`, `capacity_fade_knee.png`, `lot_release.pdf`.

## 10. Where 25+ rubric criteria come from

* Model coefficients (2), training RMSE, predicted lives for ~40 lot cells (spot-check 15), failure count, decision, linear
  extrapolation contrast.

## 11. Golden-output checklist

* Correct ΔQ variance feature; training-only fit; lot predictions; threshold; decision.

## 12. Build notes (scope tuning)

* Reproduce the paper's variance-model coefficients approximately before freezing; document any cells excluded by the paper.
* If the published secondary batch passes comfortably, set the warranty cycle threshold (e.g. 600 vs 700) before writing the
  prompt so that the decision is non-trivial — and keep it fixed.
