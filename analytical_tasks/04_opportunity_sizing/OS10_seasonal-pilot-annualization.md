# OS10 — Annualising a summer pilot: twelve times July is not a year

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Sizing a product's annual value from a pilot that ran in its best season (summer promotions, holiday launches, back-to-school features) |
| Domain | Urban mobility / bike share |
| Task shape | 02 · Forecast across many periods (monthly e-bike trips for the next 12 months from a June–August pilot; the fleet expansion level committed) |
| Core method | Estimate the pilot's share of system trips (e-bike share of trips in pilot months, by member type) and apply it to each future month's system forecast built from seasonal indices of prior years; adoption ramp per memo; revenue by member type (members pay per minute differently) |
| Analytical stump | Multiplying peak-month pilot trips by 12 assumes every month looks like summer; bike-share demand falls steeply in winter, and casual riders (who pay most per ride) vanish faster than members. Seasonal indices by member type turn a pilot into an annual estimate |
| Primary sources | Bluebikes (Boston metro bike share) monthly trip history data |

## 1. The real-world situation

A bike-share operator ran an e-bike pilot from June to August. The product manager annualised pilot revenue as 4 × the summer quarter and
proposed expanding the e-bike fleet to 1,500 bikes. Finance asked for a month-by-month forecast that respects seasonality and the mix of
members and casual riders.

## 2. The decision (one deterministic recommendation)

**The committed e-bike fleet size (from the memo's options 500 / 1,000 / 1,500) — the largest whose annual e-bike revenue covers the fleet's
annual cost — with the monthly trip and revenue forecast.**

Rules (finance memo):

* Data: Bluebikes trip histories for the three prior years plus the pilot year; e-bike trips identified by `rideable_type` = electric_bike
  (pilot months).
* Seasonal index by member type: month share of annual trips averaged over the three prior years.
* Pilot share: e-bike trips ÷ all trips in pilot months, by member type.
* Future system trips by month = last full year's trips by member type × (1 + growth from memo) distributed by seasonal index.
* E-bike trips = system trips × pilot share (member-type specific) × fleet scaling factor for the option (memo's capacity curve).
* Revenue per trip by member type (memo price table); annual revenue = Σ months.
* Annual cost per option from `fleet_costs.json`; choose the largest option with revenue ≥ cost.

## 3. Why capable analysts get it wrong

* Pilots run in favourable seasons; annualising linearly is common.
* Member mix shifts across seasons; casual riders are concentrated in summer.
* Pilot share should be applied to a seasonal base, not to summer volumes.
* Fleet scaling has diminishing returns (capacity curve).

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–48 | `<yyyymm>-bluebikes-tripdata.csv` (4 years) | CSV | ~100k–450k each | Bluebikes system data | Bluebikes data license agreement (public reuse) | Trips with member type, rideable type |
| 49 | `current_bluebikes_stations.csv` | CSV | ~500 | Bluebikes | Same | Stations |
| 50 | `price_table.json` | JSON | — | Task author (from public pricing pages) | — | Revenue per trip |
| 51 | `fleet_costs.json` | JSON | 3 | Task author | — | Costs |
| 52 | `capacity_curve.json` | JSON | 3 | Task author | — | Fleet scaling factors |
| 53 | `finance_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 54 | `pm_annualisation.xlsx` | XLSX | — | Task author | — | Naive annualisation |
| 55 | `monthly_trips_by_type.parquet` | Parquet | ~200 | Derived | Same | Convenience |

## 5. Deterministic solution path

1. Monthly trips by member type for prior years; seasonal indices.
2. Pilot shares by member type.
3. Monthly forecasts per fleet option; revenue; cost comparison; choose.
4. Contrast with the 4 × summer annualisation.

## 6. Wrong paths (method errors, not misreadings)

**A — 4 × summer quarter.** Overstated revenue.

**B — single seasonal index for all riders.** Mix effects lost.

**C — pilot share applied to annual totals ignoring member type.** Revenue misstated.

**D — linear fleet scaling.** Ignores capacity curve.

## 7. Why the stump is analytical, not semantic

Indices, shares and prices are specified. The trap is extrapolating from a seasonal peak.

## 8. Draft task prompt (prose)

> How big should the e-bike fleet be? Turn the summer pilot into a 12-month forecast using seasonal indices by rider type, as the finance memo
> specifies, and compare revenue with fleet costs. Provide `ebike_forecast.csv` (month × option: trips, revenue), `seasonal_forecast.png`, and a
> one-page `fleet_commitment.pdf`.

## 9. Deliverables

* `ebike_forecast.csv`, `seasonal_forecast.png`, `fleet_commitment.pdf`.

## 10. Where 25+ rubric criteria come from

* 12 months × chosen option (trips, revenue) = 24; annual revenue per option; choice; PM contrast.

## 11. Golden-output checklist

* Seasonal indices; member-type shares; capacity curve; prices; costs; choice.

## 12. Build notes (scope tuning)

* Confirm the PM's method supports 1,500 bikes while the seasonal forecast supports a smaller option.
