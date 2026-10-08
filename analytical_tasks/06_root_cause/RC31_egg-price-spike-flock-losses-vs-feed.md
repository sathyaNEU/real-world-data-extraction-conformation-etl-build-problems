# RC31 — Egg prices tripled: feed costs, producer pricing, or avian-flu flock losses working through with a lag?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Supply-driven price spikes with delayed recovery (memory-chip prices after fab outages, GPU rental prices after supply shocks, used-car prices after chip shortages), where a contemporaneous correlate takes the blame |
| Domain | Food supply chain / grocery pricing |
| Task shape | 17 · Periods around a change point (egg prices before, during and after avian-influenza waves; the break dated and attributed with distributed lags of layer losses versus feed costs) |
| Core method | Monthly panel of table-egg layer inventory, layer losses from confirmed highly pathogenic avian influenza (HPAI) detections, feed cost index and retail and wholesale egg prices; distributed-lag regression of log wholesale price on the layer inventory gap (actual vs pre-outbreak seasonal trend, lags 0–3) and log feed cost (lags 0–6), with month-of-year effects; date the regime break with a Bai–Perron test; attribute the price rise between the pre-break and peak periods with the fitted terms |
| Analytical stump | Feed costs rose in the same year, so a same-month correlation between egg prices and feed costs looks convincing. The supply shock acts through the layer inventory, which falls when flocks are depopulated and recovers only after months of repopulation; prices respond to the inventory gap, not to the count of detections in a month. Using total hens (including hatchery flocks) or detections without flock size also dilutes the signal |
| Primary sources | USDA NASS Chickens and Eggs (monthly layers and production); USDA APHIS confirmed HPAI detections in commercial and backyard flocks; USDA AMS egg market reports (wholesale prices); BLS average retail price for eggs; USDA ERS feed grains database |

## 1. The real-world situation

A grocery chain faced public criticism over egg prices. Its pricing team's internal note blamed producers' feed costs and suggested negotiating
supplier cost pass-through clauses. The supply-chain team believed avian-influenza flock losses were the driver and that prices would ease only as
flocks were rebuilt. Leadership wanted to know which story the data supports before choosing a supplier strategy.

## 2. The decision (one deterministic recommendation)

**The primary driver of the price rise from the pre-break period to the peak (layer-inventory gap or feed costs, by fitted contribution), with the
dated break and the lag at which the inventory gap has its largest effect.**

Rules (supply-chain memo):

* Data: monthly NASS table-egg layers (all layers excluding hatchery-supply flocks, per the memo's series); APHIS detections with flock type and
  birds affected (commercial table-egg layers only, summed by month of confirmation); AMS weekly wholesale price for large white eggs (memo's market
  series) averaged by month; BLS average retail price (eggs, grade A large, per dozen); ERS monthly corn and soybean-meal prices combined into the
  memo's layer-feed index.
* Pre-outbreak trend: seasonal-trend model of layers (month-of-year means plus linear trend) fitted on the 36 months before the first commercial
  table-egg detection; inventory gap = (actual − trend) ÷ trend.
* Regression: log wholesale price on gap lags 0–3, log feed index lags 0–6 and month-of-year effects; Newey–West standard errors (lag 3).
* Break dating: Bai–Perron on log wholesale price (one break, 15% trimming).
* Attribution between the 12 months before the break and the 3 peak months: contribution of each driver = Σ coefficients × change in the driver's
  lagged values (fitted); residual reported.
* Primary driver = larger contribution.

## 3. Why capable analysts get it wrong

* Feed costs and egg prices rose together in the same months.
* Flock losses act through an inventory stock with slow recovery.
* Detection counts ignore flock size; total hens include birds that do not lay table eggs.
* Seasonal holiday demand overlays the shock.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `nass_chickens_and_eggs_<years>.csv` | CSV | ~20k series-months | USDA NASS Quick Stats (Chickens and Eggs) | U.S. Government work (public domain) | Layers and production |
| 2 | `aphis_hpai_detections.csv` | CSV | ~1,500 detections | USDA APHIS confirmed HPAI detections | Public domain | Flock losses |
| 3 | `ams_egg_markets_weekly_<years>.csv` | CSV | ~5k | USDA AMS Market News | Public domain | Wholesale prices |
| 4 | `bls_apu0000708111.csv` | CSV | ~500 | BLS average price data | Public domain | Retail price |
| 5 | `ers_feed_grains_monthly.xlsx` | XLSX | ~3k | USDA ERS Feed Grains Database | Public domain | Corn and soybean meal |
| 6 | `supply_chain_memo.pdf` | PDF | — | Task author | — | Rules in §2, feed index weights |
| 7 | `pricing_team_feed_note.xlsx` | XLSX | — | Task author | — | Same-month correlation |

## 5. Deterministic solution path

1. Build the monthly panel; filter commercial table-egg detections; feed index.
2. Fit the pre-outbreak layer trend; compute the inventory gap.
3. Distributed-lag regression; coefficients and lag profile.
4. Bai–Perron break; attribution between the windows; primary driver.
5. Contrast with the pricing team's correlation.

## 6. Wrong paths (method errors, not misreadings)

**A — same-month correlation with feed costs.** Confounded co-movement credits feed.

**B — detections count as the driver.** Ignores flock size and the inventory stock dynamics.

**C — total hens.** Hatchery flocks dilute the table-egg inventory gap.

**D — no seasonal terms.** Holiday demand peaks are attributed to the shock or to feed.

## 7. Why the stump is analytical, not semantic

The series, filters and model are specified. The trap is a stock-mediated supply shock with lags versus a contemporaneous correlate.

## 8. Draft task prompt (prose)

> Our pricing team blames feed costs for the egg price spike; supply chain blames avian flu. Use the supply-chain memo's distributed-lag model to tell
> me what drove the rise and when the break occurred. Provide `egg_price_attribution.csv` (driver: contribution, lag profile), `egg_price_timeline.png`,
> and a one-page `egg_price_rca.pdf`.

## 9. Deliverables

* `egg_price_attribution.csv` — coefficients by lag, contributions and residual.
* `egg_price_timeline.png` — prices, inventory gap and feed index on aligned axes with the break marked.
* `egg_price_rca.pdf` — primary driver, break date, peak-effect lag, and the pricing-team contrast.

## 10. Where 25+ rubric criteria come from

* Panel construction (filters, feed index, monthly averaging): 5.
* Trend fit and gap series: 3.
* Coefficients for gap lags (4) and feed lags (7) with significance: 11.
* Break date: 1.
* Contributions, residual and primary driver: 4.
* Contrast: 2.

## 11. Golden-output checklist

* Commercial table-egg detections only; layer series excluding hatchery supply.
* 36-month pre-outbreak trend; gap definition.
* Lag structure; Newey–West; Bai–Perron settings.

## 12. Build notes (scope tuning)

* Use the 2022–2023 HPAI waves; confirm that the inventory-gap contribution dominates while the same-month feed correlation exceeds 0.6.
