# AD09 — Which fuel brands kept the tax cut? Event-logged prices must be averaged over time, not over events

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Mirrors | Time-weighting event-logged data (price-change logs, configuration-change logs, status histories), where averaging records weights by change frequency instead of duration |
| Domain | Competition / consumer protection / retail fuel markets |
| Task shape | 07 · Grid of cells (brand × federal state relative margin change → the anomalous cell) |
| Core method | Duration-weighted (time-weighted) average prices from price-change event logs; local-peer relative pricing; before/during comparison of relative position against a peer median |
| Analytical stump | Stations publish a new record only when they change price. Averaging the records weights each price by how often a station changes price, not by how long the price was in force; with Germany's strong intraday price cycle this biases averages by several cents — larger than the anomalies sought |
| Primary sources | Tankerkönig (MTS-K) historical price and station data, German energy-tax discount legislation (2022) |

## 1. The real-world situation

Between June and August 2022 Germany cut the energy tax on petrol and diesel. A consumer-protection agency wants to know
whether any brand, in any federal state, **raised its prices relative to local competitors** during the discount — i.e.
kept part of the cut. The analyst averaged all price records per station per day and compared May with June–August. Two
brands that change prices many times a day — mostly downward in the evening — appeared to be exceptionally cheap; one
brand that rarely changes price appeared expensive.

## 2. The decision (one deterministic recommendation)

**Which brand × state cell shows the largest increase in relative price (E5 petrol) from the pre-period to the discount
period, and does it exceed the 2.0 ct/l referral threshold?**

Rules (market monitoring memo):

* Price records from the Tankerkönig/MTS-K history; station metadata from the matching station file. Fuel: E5.
* Station daily price = **time-weighted** average over 07:00–22:00 local time, each price weighted by the minutes it was in
  force (the price at 07:00 is the last record before 07:00).
* Local peer median = median daily price of all other stations within 5 km (great-circle) that have prices that day.
* Relative price = station daily price − local peer median. Period means over 2022-05-01 to 05-31 (pre) and 2022-06-01 to
  08-31 (discount).
* Cell value = mean over the cell's stations of (discount mean − pre mean); cells need ≥ 30 stations.
* Refer the maximum cell if it exceeds 2.0 ct/l.

## 3. Why capable analysts get it wrong

* Event logs look like samples of a price, so `mean(price)` per day feels right; it is a mean over changes, not over time.
* German stations change prices many times a day with a steep evening decline; frequent changers have many low-price
  records.
* Comparing levels across regions ignores local competition; relative-to-peer comparisons isolate conduct.
* The tax cut moves every price; the anomaly is in the relative position, not in the level change.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–123 | `prices/2022/05/2022-05-01-prices.csv` … `2022/08/2022-08-31-prices.csv` (daily files) | CSV | 300k–500k each | Tankerkönig historic data (MTS-K) | CC BY 4.0 | Price-change records |
| 124 | `stations/2022-05-01-stations.csv` | CSV | ~15k | Tankerkönig | CC BY 4.0 | Brand, coordinates, state (via postcode) |
| 125 | `postcode_to_state_de.csv` | CSV | ~8k | Open postcode reference (verify licence) | Open | Federal state mapping |
| 126 | `energiesteuer_temporary_reduction_2022.pdf` | PDF | — | German federal law gazette (Bundesgesetzblatt) extract | Public law | Discount amounts and dates |
| 127 | `mts_k_overview.pdf` | PDF | — | Bundeskartellamt Market Transparency Unit for Fuels | Public | How prices are reported |
| 128 | `monitoring_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 129 | `analyst_event_mean_results.xlsx` | XLSX | ~200 | Task author | — | Event-averaged first attempt |
| 130 | `brand_normalization.json` | JSON | ~50 | Task author | — | Brand name variants → brand |

## 5. Deterministic solution path

1. For each station-day, reconstruct the price step function and compute the 07:00–22:00 time-weighted mean.
2. Build 5 km peer sets; compute daily peer medians and relative prices.
3. Period means; per-station change; aggregate to brand × state cells with ≥ 30 stations.
4. Identify the maximum cell; apply the 2.0 ct/l threshold.
5. Contrast with event-averaged daily prices.

## 6. Wrong paths (method errors, not misreadings)

**A — event-averaged prices.** Frequent changers look cheap; the anomalous cell changes.

**B — level changes instead of relative prices.** Everyone fell by roughly the tax cut; regional crude/transport differences
dominate.

**C — 24-hour averaging including night.** Few transactions at night; distorts the relevant price.

**D — peers including the station itself.** Dampens relative changes.

## 7. Why the stump is analytical, not semantic

Every record is "price changed to X at time t" and the memo defines the averaging window and peer set. The error is
statistical — computing an unweighted mean of an irregularly sampled step function.

## 8. Draft task prompt (prose)

> We need to know whether any brand, in any state, raised its petrol prices relative to nearby competitors while the 2022
> fuel tax discount was in force, measured the way the monitoring memo specifies. Using the Tankerkönig price and station
> files in the folder, compute each station's time-weighted daily price and its position against local peers, aggregate to
> brand by state, and tell me the top cell and whether it crosses the referral threshold. Produce `relative_price_grid.csv`
> (brand × state: stations, pre and discount relative price, change) and `relative_price_heatmap.png` with the referred cell
> outlined. Add a one-page `referral_memo.pdf` with the answer and how the event-averaged analysis misjudged the frequent
> price changers.

## 9. Deliverables

* `relative_price_grid.csv`, `relative_price_heatmap.png`, `referral_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* Grid cells (e.g. 6 brands × 6 states = 36, eligible ones checked); top cell value and referral; event-average contrast for
  2 brands.

## 11. Golden-output checklist

* Time-weighted 07–22 averages; 5 km peers excluding self; relative change; cell minimums; threshold applied.

## 12. Build notes (scope tuning)

* Verify that the event-mean vs time-weighted difference exceeds 2 ct/l for at least one frequent-changing brand.
* Tankerkönig data are large; ship only the months needed and document the download source and licence attribution.
