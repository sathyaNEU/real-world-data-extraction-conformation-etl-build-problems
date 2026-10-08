# FC03 — Forecasting slow-moving spare parts: the "most accurate" method is the one that empties the shelf

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Automotive/aftermarket and device-repair parts planning (dealer networks, authorized repair centres) |
| Domain | Spare-parts inventory planning |
| Task shape | 07 · Grid of cells (demand segment × forecasting method → replayed inventory cost; best method per row) |
| Core method | Demand-pattern classification (ADI/CV²), intermittent-demand methods (Croston, SBA), out-of-sample replay of an order-up-to policy driven by each forecast |
| Analytical stump | For intermittent demand, point-accuracy metrics (MAE) reward forecasts near zero and MAPE is undefined on zero months; the method must be chosen by the decision's loss. Croston is biased upward; SBA corrects it |
| Primary sources | "carparts" monthly demand of 2,674 car parts (Hyndman et al., distributed in the R package expsmooth) |

## 1. The real-world situation

A car-parts distributor is moving its long tail of slow-moving parts to a monthly replenishment engine. Planning ran a
bake-off of forecasting methods and picked the winner per demand segment by mean absolute error. In the lumpy segment the
winner forecast almost nothing; the engine then held almost no stock, and fill rates collapsed within a quarter.

## 2. The decision (one deterministic recommendation)

**Which forecasting method should the engine use for each demand segment, and what total inventory cost does that
configuration produce over the 12-month evaluation?**

Rules (planning memo):

* Series: monthly demand for each part (Jan 1998 – Mar 2002). Parts in scope: complete series with ≥ 10 non-zero months in
  the first 39 months (training); evaluation = the last 12 months.
* Segments on training data (Syntetos–Boylan cut-offs ADI 1.32, CV² 0.49): smooth, erratic, intermittent, lumpy.
* Candidate methods, α = 0.1, initialized on the first 12 training months: zero forecast, naive, SES, Croston, SBA
  (Croston × (1 − α/2)).
* Engine (as implemented): monthly review, lead time 1 month, order-up-to S = 2 × f + 1.645 × RMSE × √2, where f is the
  current one-month-ahead forecast and RMSE is the root-mean-square one-step error over the preceding 24 months; unmet demand
  is lost.
* Costs (unit-free, per part): holding 0.02 per unit-month on stock at month end; lost sale 1.0 per unit.
* Adopt for each segment the method with the lowest total cost across its parts in the evaluation months.

## 3. Why capable analysts get it wrong

* Accuracy bake-offs are the default way to choose methods.
* With many zero months the median demand is zero, so MAE favours forecasts near zero — which the engine turns into near-zero
  stock.
* MAPE divides by zero on zero-demand months; dropping them silently changes the comparison.
* Croston looks tailor-made for intermittent demand but is biased upward; the SBA correction matters for cost.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `carparts.csv` (wide: 2,674 parts × 51 months) | CSV | 2,674 | R package `expsmooth` (Hyndman et al.) | GPL (package; verify data terms) | Monthly demand |
| 2 | `carparts_long.parquet` | Parquet | ~136k part-months | Derived | Same | Long format |
| 3 | `carparts_long.json` (sample of 200 parts) | JSON | ~10k | Derived | Same | API-style sample |
| 4 | `hyndman_forecasting_with_exponential_smoothing_ch16_extract.pdf` (citation) | PDF | — | Springer 2008 (cite) | Cite | Data provenance |
| 5 | `syntetos_boylan_classification.pdf` (citation) | PDF | — | Published paper (cite) | Cite | Segment cut-offs |
| 6 | `croston_sba_reference.pdf` (citation) | PDF | — | Published papers (cite) | Cite | Method definitions |
| 7 | `replenishment_engine_spec.pdf` | PDF | — | Task author | — | Policy formula |
| 8 | `cost_parameters.json` | JSON | — | Task author | — | Holding and lost-sale costs |
| 9 | `planning_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 10 | `accuracy_bakeoff_results.xlsx` | XLSX | ~20 | Task author | — | The MAE-based selection |

## 5. Deterministic solution path

1. Select parts; classify segments on training data.
2. For each part and method, generate one-step forecasts through the evaluation months.
3. Replay the engine month by month (inventory position, orders arriving after one month, lost sales) per method.
4. Sum holding + lost-sale costs per segment × method (20 cells); choose the minimum per segment.
5. Also compute MAE per cell to show where accuracy and cost disagree.

## 6. Wrong paths (method errors, not misreadings)

**A — choose by MAE.** Zero/near-zero forecasts win in intermittent and lumpy segments; lost-sale cost explodes.

**B — choose by MAPE with zero months dropped.** Favours naive/SES; mis-specified comparison.

**C — Croston without bias correction.** Over-stocks; SBA is cheaper.

**D — in-sample evaluation.** Methods compared on training fit; ranks change out of sample.

## 7. Why the stump is analytical, not semantic

Demand, segments, methods, engine and costs are all specified. The error is the evaluation criterion: an accuracy score that
is mathematically biased toward zero for intermittent series, instead of the loss the business incurs.

## 8. Draft task prompt (prose)

> We're configuring the monthly replenishment engine for our slow movers and need one forecasting method per demand segment —
> the one that gives the lowest inventory cost when the engine runs on it, per the planning memo and engine spec. Run every
> candidate through the 12 evaluation months for every in-scope part and tell me which method each segment should use and the
> total cost. Deliver `method_cost_grid.xlsx` (segment × method: holding cost, lost-sale cost, total, MAE; parts per segment)
> and `cost_vs_accuracy.png` plotting each cell's MAE against its total cost with the adopted cells highlighted. On the first
> sheet, state the adopted method per segment, the total cost, and how much more the MAE-based selection would cost.

## 9. Deliverables

* `method_cost_grid.xlsx`, `cost_vs_accuracy.png`.

## 10. Where 25+ rubric criteria come from

* 4 segments × 5 methods = 20 cost cells; adopted method per segment (4); total cost; MAE-selection penalty.

## 11. Golden-output checklist

* Correct segmentation; SBA correction; engine replay with lead time and lost sales; per-segment minimum cost.

## 12. Build notes (scope tuning)

* Confirm MAE picks a different method than cost in at least two segments under the stated cost ratio.
* Publish the in-scope part list and a reference replay for one part.
