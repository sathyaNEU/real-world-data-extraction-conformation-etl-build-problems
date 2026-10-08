# RC07 — Why did imbalance prices spike? Wind forecast misses, plant trips and demand errors leave different fingerprints

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Cost spikes from forecast misses versus supply failures (cloud spot prices, ride-hail surge, inventory expediting costs) |
| Domain | Electricity balancing markets |
| Task shape | 18 · Hypotheses versus evidence (spike settlement periods × causes: wind forecast error, unplanned generator outage, demand forecast error, interconnector change → evidence cells; the dominant cause across the month's spikes) |
| Core method | For each settlement period with system price above the memo's spike threshold: wind error = day-ahead wind forecast − outturn; demand error = day-ahead demand forecast − outturn; unplanned outages from REMIT messages starting within the prior 2 hours (MW lost); interconnector flow change versus schedule; classify each spike by the largest normalised imbalance contribution (MW) above thresholds; aggregate counts and £ impact |
| Analytical stump | Correlating monthly average prices with monthly wind output says little about spikes. Individual spikes have different causes; aligning each half-hour with the forecast errors and outage messages active at that time is required. Counting spikes without weighting by severity also misleads |
| Primary sources | Elexon BMRS / Insights data (system prices, wind and demand forecasts and outturn, interconnector flows) and REMIT outage messages |

## 1. The real-world situation

A supplier saw imbalance costs triple in one winter month. The trading desk blamed low wind. Operations suspected a cluster of large unplanned plant
outages. The CFO asked which cause dominated the spikes that drove the cost.

## 2. The decision (one deterministic recommendation)

**The dominant cause of the month's price spikes (by share of spike-period £ impact weighted by the system's net imbalance volume), with the
cause × spike evidence grid.**

Rules (trading memo):

* Data: BMRS system buy/sell prices per settlement period for the month; day-ahead wind forecast and outturn; day-ahead demand forecast (INDO/TSD per
  memo) and outturn; interconnector flows and schedules; REMIT unavailability messages (unplanned) for generators ≥ 100 MW.
* Spike: system price ≥ £300/MWh.
* Contributions (MW): wind shortfall = max(0, forecast − outturn); demand excess = max(0, outturn − forecast); outage = Σ unplanned MW lost with
  event start within the prior 2 hours and still active; interconnector shortfall = max(0, scheduled import − actual).
* Classify each spike by the largest contribution; ties by earlier listed cause.
* Impact per spike = |net imbalance volume (NIV)| for the period × (price − £100 reference).
* Dominant cause = largest impact share.

## 3. Why capable analysts get it wrong

* Monthly correlations hide event-level causes.
* Forecast errors, not output levels, drive imbalance.
* Outage messages must be time-aligned to settlement periods.
* Impact weighting matters more than spike counts.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `system_prices_<month>.csv` | CSV | ~1,500 periods | Elexon BMRS/Insights API | BMRS data licence (open; attribution) | Prices |
| 2 | `wind_forecast_outturn_<month>.csv` | CSV | ~3k | Elexon BMRS | Same | Wind forecasts and outturn |
| 3 | `demand_forecast_outturn_<month>.csv` | CSV | ~3k | Elexon BMRS | Same | Demand |
| 4 | `interconnector_flows_<month>.csv` | CSV | ~15k | Elexon BMRS | Same | Flows and schedules |
| 5 | `remit_messages_<month>.json` | JSON | ~5k | Elexon REMIT | Same | Unplanned outages |
| 6 | `net_imbalance_volume_<month>.csv` | CSV | ~1,500 | Elexon BMRS | BMRS data licence | NIV per settlement period |
| 7 | `trading_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 8 | `desk_wind_explanation.xlsx` | XLSX | — | Task author | — | Desk's analysis |

## 5. Deterministic solution path

1. Identify spike periods; compute contributions per period.
2. Classify; impacts; aggregate by cause.
3. Evidence grid; dominant cause; contrast with desk explanation.

## 6. Wrong paths (method errors, not misreadings)

**A — monthly wind–price correlation.** Wrong level of analysis.

**B — wind outturn level instead of forecast error.** Wrong driver.

**C — REMIT messages not time-aligned.** Misattributed outages.

**D — counting spikes equally.** Ignores impact.

## 7. Why the stump is analytical, not semantic

The thresholds, contributions and classification are specified. The trap is aggregating away event-level causality.

## 8. Draft task prompt (prose)

> What drove the imbalance cost spike this month? Attribute each price spike to its cause using forecast errors and outage messages as the trading memo
> specifies. Provide `spike_evidence.csv` (period: price, contributions, cause, impact), `spike_timeline.png`, and a one-page `imbalance_rca.pdf`.

## 9. Deliverables

* `spike_evidence.csv`, `spike_timeline.png`, `imbalance_rca.pdf`.

## 10. Where 25+ rubric criteria come from

* Spike count; classification of each spike (sampled 15); impact by cause (4); dominant cause; desk contrast.

## 11. Golden-output checklist

* Threshold; contributions; time alignment; ties; impact weighting.

## 12. Build notes (scope tuning)

* Choose a month with both low-wind periods and a cluster of large trips; confirm the desk's explanation is not dominant by impact.
