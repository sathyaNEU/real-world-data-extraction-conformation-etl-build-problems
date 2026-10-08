# FC03 — Forecasting slow movers: the "most accurate" method is the one that empties the shelf

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Domain | Wholesale distribution / inventory planning |
| Task shape | 07 · Grid of cells (demand segment × forecasting method → replayed inventory cost; best method per row) |
| Core method | Demand-pattern classification (ADI/CV²), intermittent-demand methods (Croston, SBA), out-of-sample replay of an order-up-to policy driven by each forecast |
| Analytical stump | For intermittent demand, point-accuracy metrics (MAE) reward forecasts near zero and MAPE is undefined on zero weeks; the method must be chosen by the decision's loss. Croston is biased upward; SBA corrects it |
| Primary sources | UCI Online Retail II (UK online wholesaler transactions, 2009–2011) |

## 1. The real-world situation

A UK gift wholesaler is moving its long tail of slow-moving SKUs to a weekly replenishment system. Planning ran a
bake-off of forecasting methods and picked the winner per demand segment by mean absolute error. In the lumpy segment the
winner forecast almost nothing; the replenishment engine then held almost no stock, and service collapsed in the first
quarter.

## 2. The decision (one deterministic recommendation)

**Which forecasting method should the replenishment system use for each demand segment, and what total inventory cost
does that configuration produce over the 26-week evaluation?**

Rules (planning memo):

* Weekly demand per SKU = Σ positive `Quantity` on non-cancelled product lines (invoices not starting with `C`; product
  stock codes only), ISO weeks.
* SKUs in scope: ≥ 10 non-zero weeks between 2009-12-07 and 2011-05-29 (training); evaluation = 26 weeks from 2011-05-30.
* Segments (Syntetos–Boylan cut-offs on training data): smooth, erratic, intermittent, lumpy (ADI 1.32, CV² 0.49).
* Candidate methods, all with α = 0.1 and initialized on the first 13 training weeks: zero forecast, naive (last week),
  SES, Croston, SBA (Croston × (1 − α/2)).
* The replenishment engine (as implemented): weekly review, lead time 2 weeks, order-up-to level
  S = 3 × f + 1.645 × RMSE × √3, where f is the current one-week-ahead forecast and RMSE is the root-mean-square one-step
  error over the preceding 26 weeks; unmet demand is lost.
* Costs: holding = 0.4% of the SKU's median unit price per unit per week; lost sale = 35% of median unit price per unit.
* Adopt for each segment the method with the lowest total cost across its SKUs in the evaluation weeks.

## 3. Why capable analysts get it wrong

* Accuracy bake-offs are the default way to choose forecasting methods.
* With many zero weeks, the median is zero, so MAE favours forecasts close to zero — which the order-up-to logic turns into
  near-zero stock.
* MAPE divides by zero on zero-demand weeks; dropping those weeks silently changes the comparison.
* Croston's method looks tailor-made for intermittent demand but is biased upward; the SBA correction matters for cost.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `online_retail_II.xlsx` | XLSX | ~1.07M lines | UCI ML Repository (id 502) | CC BY 4.0 | Transactions |
| 2 | `online_retail_II_2010_2011.csv` | CSV | ~0.54M | Derived from #1 | CC BY 4.0 | Same, CSV |
| 3 | `weekly_demand_long.parquet` | Parquet | ~200k SKU-weeks | Derived from #1 | CC BY 4.0 | Weekly series |
| 4 | `non_product_stockcodes.json` | JSON | ~15 | Task author | — | Exclusions |
| 5 | `syntetos_boylan_classification.pdf` | PDF | — | Published paper (cite) | Cite | Segment cut-offs |
| 6 | `croston_sba_reference.pdf` | PDF | — | Published papers (cite) | Cite | Method definitions |
| 7 | `replenishment_engine_spec.pdf` | PDF | — | Task author | — | Policy formula |
| 8 | `cost_parameters.json` | JSON | — | Task author | — | Holding and lost-sale rates |
| 9 | `planning_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 10 | `accuracy_bakeoff_results.xlsx` | XLSX | ~20 | Task author (the MAE-based selection) | — | Baseline to beat |

## 5. Deterministic solution path

1. Build weekly SKU series; select SKUs; classify segments on training data.
2. For each SKU and method, generate one-step forecasts through the evaluation period.
3. Replay the engine week by week (inventory position, orders arriving after 2 weeks, lost sales) for each method.
4. Sum holding + lost-sale costs per segment × method (20 cells); choose the minimum per segment.
5. Also compute MAE per cell to show where accuracy and cost disagree.

## 6. Wrong paths (method errors, not misreadings)

**A — choose by MAE.** Zero/near-zero forecasts win in intermittent and lumpy segments; lost-sale cost explodes.

**B — choose by MAPE with zero weeks dropped.** Favors naive/SES; mis-specifies the comparison.

**C — Croston without bias correction as the "intermittent" default.** Over-stocks; SBA is cheaper.

**D — in-sample evaluation.** Methods compared on training fit; ranks change out of sample.

## 7. Why the stump is analytical, not semantic

Demand, segments, methods, the engine and costs are all specified. The error is choosing the evaluation criterion: an
accuracy score that is mathematically biased toward zero for intermittent series, instead of the loss the business
actually incurs.

## 8. Draft task prompt (prose)

> We're configuring the weekly replenishment system for our slow movers and need one forecasting method per demand
> segment — the one that gives the lowest inventory cost when the engine runs on it, per the planning memo and engine spec
> in the folder. Run every candidate method through the 26 evaluation weeks for every in-scope SKU and tell me which method
> each segment should use and the total cost of that configuration. Deliver `method_cost_grid.xlsx` with the
> segment-by-method grid of holding cost, lost-sale cost, total cost and MAE, plus SKU counts per segment, and
> `cost_vs_accuracy.png` plotting each cell's MAE against its total cost with the adopted cells highlighted. On the first
> sheet, state the adopted method per segment, the total cost, and how much more the MAE-based selection would have cost.

## 9. Deliverables

* `method_cost_grid.xlsx`, `cost_vs_accuracy.png`.

## 10. Where 25+ rubric criteria come from

* 4 segments × 5 methods = 20 cost cells; adopted method per segment (4); total cost; MAE-selection penalty.

## 11. Golden-output checklist

* Correct segmentation; SBA correction; engine replay with lead time and lost sales; per-segment minimum cost.

## 12. Build notes (scope tuning)

* Tune the lost-sale/holding ratio only within a realistic range (stated in the memo) and confirm MAE picks a different
  method than cost in at least two segments.
* Fix weekly bucketing (ISO weeks) and initialization rules exactly; publish the SKU list used.
