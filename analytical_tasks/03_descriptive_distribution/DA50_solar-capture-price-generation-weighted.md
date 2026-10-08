# DA50 — What solar actually earned: the time-weighted average price is not the price solar captured

| Field | Value |
|---|---|
| Category | Descriptive & Distribution Analysis |
| Mirrors | Revenue analytics where volume and price co-move (traffic-weighted versus time-weighted cost, ad revenue when inventory peaks at low CPMs, ride-hail earnings by hour) |
| Domain | Electricity markets / renewable investment |
| Task shape | 07 · Grid of cells (5 regions × 4 years → time-weighted average price, solar capture price, capture ratio; the region where a solar-plus-storage project is prioritised) |
| Core method | Capture price = Σ (5-minute price × solar output) ÷ Σ solar output, using regional utility-scale solar SCADA generation; capture ratio = capture price ÷ time-weighted average price; negative-price intervals included; comparison with time-weighted averages |
| Analytical stump | Solar produces when many solar farms produce, depressing prices (cannibalisation) — sometimes below zero. A time-weighted average price overstates what solar earns; the gap differs by region and grows with penetration. Investment screens using average prices pick the wrong region |
| Primary sources | AEMO (Australian Energy Market Operator) NEM dispatch prices and unit SCADA data (MMS Data Model archive / NEMWEB) |

## 1. The real-world situation

A developer prioritises one NEM region for a solar-plus-storage project, preferring regions where solar captures the most value (storage is
sized later). The screening model used annual time-weighted average prices and ranked a region with high average prices first. An analyst
noted that midday prices in that region are frequently negative.

## 2. The decision (one deterministic recommendation)

**The prioritised region: highest 2023 solar capture price, with the 5 × 4 grid of time-weighted prices, capture prices and capture ratios
(2020–2023).**

Rules (investment memo):

* Prices: regional reference price (RRP) at 5-minute dispatch intervals (from DISPATCHPRICE; intervention pricing excluded per memo).
* Solar output: Σ SCADA MW of utility-scale solar units in the region (DUIDs classified as solar in the registration list) per interval.
* Capture price = Σ RRP × MW ÷ Σ MW (intervals with MW > 0).
* Time-weighted average = mean RRP over all intervals.
* Capture ratio = capture ÷ time-weighted.
* Priority: highest 2023 capture price.

## 3. Why capable analysts get it wrong

* Average prices are the standard market summary.
* Correlation between solar output and price lowers realised value.
* Negative prices must be included, not floored at zero.
* Region-level solar shape matters; using a generic solar profile misses curtailment and local patterns.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–48 | `PUBLIC_DVD_DISPATCHPRICE_<yyyymm>.zip` (2020–2023) | CSV inside ZIP | ~45k intervals × 5 regions per month | AEMO NEMWEB MMS archive | AEMO copyright permissions (use with attribution) | 5-minute prices |
| 49–96 | `PUBLIC_DVD_DISPATCH_UNIT_SCADA_<yyyymm>.zip` | CSV inside ZIP | ~3–4M per month | AEMO | Same | Unit MW by interval |
| 97 | `NEM_Registration_and_Exemption_List.xlsx` | XLSX | ~1k units | AEMO | Same | DUID fuel type, region |
| 98 | `mms_data_model_report.pdf` | PDF | — | AEMO | Same | Table definitions |
| 99 | `investment_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 100 | `screening_model_avg_prices.xlsx` | XLSX | 5 | Task author | — | Screening ranking |
| 101 | `solar_duids.csv` | CSV | ~100 | Derived | Same | Solar units by region |
| 102 | `capture_price_check.json` | JSON | ~5 | Task author | — | One-day check values |

## 5. Deterministic solution path

1. Load prices; exclude intervention intervals; load SCADA for solar DUIDs; sum by region and interval.
2. Join prices and output; compute capture and time-weighted prices by region-year.
3. Capture ratios; choose region; contrast with the screening model.

## 6. Wrong paths (method errors, not misreadings)

**A — time-weighted averages.** Overstate solar value.

**B — flooring negative prices at zero.** Overstates capture.

**C — generic solar profile.** Misses regional shapes.

**D — including rooftop solar estimates instead of SCADA units.** Not the memo's definition.

## 7. Why the stump is analytical, not semantic

The tables and formula are specified. The trap is ignoring the covariance between quantity and price in an average.

## 8. Draft task prompt (prose)

> Which NEM region should we prioritise for the solar-plus-storage project? Compute generation-weighted solar capture prices and capture ratios
> as the investment memo specifies. Provide `capture_grid.csv` (region × year: time-weighted price, capture price, ratio), `capture_ratio_trend.png`,
> and a one-page `region_priority.pdf`.

## 9. Deliverables

* `capture_grid.csv`, `capture_ratio_trend.png`, `region_priority.pdf`.

## 10. Where 25+ rubric criteria come from

* 20 cells × 3 values (sampled 30); priority; contrast; negative-price share.

## 11. Golden-output checklist

* Intervention exclusion; solar DUID set; interval join; formula; choice.

## 12. Build notes (scope tuning)

* Confirm the highest time-weighted price region differs from the highest capture price region in 2023.
