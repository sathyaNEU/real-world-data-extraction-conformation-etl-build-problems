# DA16 — Did home prices fall? The median sale changed because different homes sold

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Home-value indices at property portals and lenders; "same-store" versus total sales growth in retail; any average-price metric exposed to mix shift |
| Domain | Real estate |
| Task shape | 03 · Bridge between two totals (median price change 2022→2023 for a city → repeat-sales index change, bridged by composition effects: property type, size, district) |
| Core method | Case–Shiller-style repeat-sales index (pairs of sales of the same property; weighted repeat-sales regression with interval-based heteroskedasticity weights); decomposition of the median change into composition shifts using cell-level medians |
| Analytical stump | Median transaction prices move when the mix of what sells changes (more small flats, fewer houses). Constant-quality price change comes from comparing the same properties over time. The median and the repeat-sales index can move in opposite directions |
| Primary sources | France "Demandes de valeurs foncières" (DVF) open data — property transactions |

## 1. The real-world situation

A mortgage lender's risk team adjusts loan-to-value haircuts by city based on the year's house-price change. For one city, the median
transaction price fell 6% from 2022 to 2023, which would trigger a higher haircut. A valuation analyst argued that 2023 sales were tilted
toward small flats and peripheral districts and that comparable homes had not fallen as much.

## 2. The decision (one deterministic recommendation)

**The constant-quality price change used for the haircut (repeat-sales index change 2022→2023, one decimal), and the bridge explaining the
gap from the median change.**

Rules (valuation memo):

* Data: DVF for the city (commune codes in the memo), 2014–2023; transactions of type "Vente" for apartments and houses, single-lot
  mutations only (one property per mutation), price > €10,000.
* Property identity: cadastral parcel + lot number (apartments) or parcel (houses), per the memo's key.
* Repeat-sales pairs: consecutive sales of the same property ≥ 6 months apart; drop pairs with annualised price change outside ±50%
  (flips/renovations per memo).
* Index: three-stage weighted repeat-sales regression (Case–Shiller): OLS on log price ratios with year dummies; regress squared residuals
  on interval length; WLS with inverse fitted variances. Index change = exp(β2023 − β2022) − 1.
* Bridge: median change → (a) property-type mix, (b) size-band mix (surface bands), (c) district mix, (d) constant-quality change (residual
  equals the repeat-sales figure difference per memo's sequential method).

## 3. Why capable analysts get it wrong

* Medians are the headline figure in most market reports.
* Composition shifts are large when market segments react differently (rates rise → fewer house sales).
* Repeat-sales indices control quality by design; their weights matter for long intervals.
* Multi-lot mutations and non-arm's-length sales distort both measures.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–10 | `valeursfoncieres-<yyyy>.txt` (2014–2023) | Pipe-delimited text | ~2.5–3.5M each (national) | DVF (data.gouv.fr, DGFiP) | Licence Ouverte / Etalab 2.0 | Transactions |
| 11 | `notice_dvf.pdf` | PDF | — | DGFiP | Licence Ouverte | Field definitions |
| 12 | `city_communes.json` | JSON | ~20 | Task author | — | Scope |
| 13 | `surface_bands.json` | JSON | 6 | Task author | — | Size bands |
| 14 | `valuation_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 15 | `risk_team_median_report.xlsx` | XLSX | ~12 | Task author | — | Median-based report |
| 16 | `case_shiller_methodology_citation.pdf` | PDF | — | S&P CoreLogic Case-Shiller methodology (cite) | Cite | Weighted repeat sales |
| 17 | `repeat_pairs.parquet` | Parquet | ~80k | Derived | Licence Ouverte | Pairs |
| 18 | `property_key_rules.json` | JSON | — | Task author | — | Identity key |

## 5. Deterministic solution path

1. Filter mutations; build property keys; select single-lot sales.
2. Median change 2022→2023; cell medians and shares for the bridge.
3. Build repeat pairs; filters; three-stage regression; index change.
4. Sequential bridge; haircut input.

## 6. Wrong paths (method errors, not misreadings)

**A — median change.** Composition-driven.

**B — hedonic-free mean of price per m².** Still mix-sensitive.

**C — unweighted repeat sales.** Long-interval pairs overweighted.

**D — multi-lot mutations included.** Price per property wrong.

## 7. Why the stump is analytical, not semantic

The keys, filters and regression are specified. The trap is composition versus constant-quality change.

## 8. Draft task prompt (prose)

> What constant-quality price change should drive this city's haircut? Build the repeat-sales index from DVF per the valuation memo and bridge
> it to the median change. Provide `price_bridge.csv` (step: amount), `index_vs_median.png` (repeat-sales index and median price 2014–2023), and a
> one-page `haircut_input.pdf`.

## 9. Deliverables

* `price_bridge.csv`, `index_vs_median.png`, `haircut_input.pdf`.

## 10. Where 25+ rubric criteria come from

* 10 annual index values; median values for 2022 and 2023; 4 bridge items; pair counts and filters; final change.

## 11. Golden-output checklist

* Single-lot filter; identity key; pair filters; three-stage weights; bridge order.

## 12. Build notes (scope tuning)

* Choose a city where the 2023 mix shifted toward small flats; confirm the index change is above −3% while the median fell ≥ 5%.
