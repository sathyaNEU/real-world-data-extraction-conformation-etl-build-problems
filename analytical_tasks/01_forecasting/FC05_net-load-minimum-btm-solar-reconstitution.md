# FC05 — Spring oversupply planning: forecasting a netted series means forecasting both of its parts

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Forecasting a netted metric whose parts follow different drivers (net revenue = gross − refunds, net adds = gross adds − churn, net load = load − rooftop solar) |
| Domain | Grid operations / renewable integration / curtailment planning |
| Task shape | 02 · Forecast across many periods (12 monthly minimum net loads → one committed planning level) |
| Core method | Component forecasting: reconstitute gross consumption by adding back behind-the-meter (BTM) solar, apply growth to the gross series, subtract next year's BTM output |
| Analytical stump | Measured load is already net of rooftop solar, whose capacity grows on its own trajectory. Growing or trend-extrapolating the net series mixes two processes with different drivers and misses the deepening midday trough |
| Primary sources | EIA-930 hourly balancing-authority data (CISO), California DG Stats NEM interconnections, CEC IEPR BTM PV projections, NREL NSRDB/PVWatts |

## 1. The real-world situation

A grid operator's planning team sets its **spring oversupply plan** (how much flexible resource and curtailment to
prepare) from the forecast lowest hourly load of 2026. The analyst took hourly load for 2023–2025, applied 1.5% annual
consumption growth and found the minimum. Operators who had watched midday load fall every spring as rooftop solar
spread said the number was far too high.

## 2. The decision (one deterministic recommendation)

**What is the committed planning level — the lowest of the twelve 2026 monthly minimum hourly net loads — and which
month sets it?**

Forecast rules (planning memo):

* "Net load" = CISO hourly demand as reported in EIA-930 (customer rooftop solar already netted out).
* Underlying customer consumption (before rooftop solar) grows 1.5% from the 2023–2025 average to 2026. Rooftop solar
  output in any hour = installed BTM AC capacity in that month × the normalized hourly PV profile for that hour.
* Installed BTM capacity: monthly cumulative from DG Stats for 2023–2025; 2026 monthly values from the CEC projection file.
* PV profile: the NSRDB-based normalized profile in the folder for each year 2023–2025 (kW per kW-AC); for 2026 use the
  hour-of-year average of the three years.
* 2026 weather/consumption pattern for each hour-of-year = average of 2023–2025 for that hour-of-year (leap day dropped).
* Monthly minimum = lowest forecast 2026 net-load hour in that month; committed level = lowest monthly minimum, rounded
  down to the nearest 100 MW.

## 3. Why capable analysts get it wrong

* The measured series is the only load series most teams have, so it is the one they forecast.
* Applying consumption growth to net load also "grows" the rooftop-solar part of the history and never adds the new
  capacity installed by 2026.
* Extrapolating the trend in monthly minima assumes rooftop growth continues at its historical pace; adoption slowed after
  the 2023 net-metering change, so a trend line overshoots.
* The fix is not a better time-series model; it is decomposing the series into parts with separate drivers.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–3 | `EIA930_CISO_2023.csv`, `…_2024.csv`, `…_2025.csv` | CSV | ~8.8k hourly each (many columns) | EIA-930 Hourly Electric Grid Monitor | U.S. Gov public domain | Net load (demand), generation by fuel |
| 4 | `eia930_ciso_2019_2025.parquet` | Parquet | ~60k | Derived | Public domain | Long history for trend comparison |
| 5 | `dgstats_nem_interconnections_monthly.csv` | CSV | ~100k installation-month rows (aggregate monthly in task) | California Distributed Generation Statistics | State of California public data (verify) | BTM capacity history |
| 6 | `cec_iepr_btm_pv_projection.xlsx` | XLSX | ~200 | California Energy Commission IEPR forecast | Public | 2026 BTM capacity |
| 7–9 | `pv_profile_2023.csv`, `pv_profile_2024.csv`, `pv_profile_2025.csv` | CSV | 8,760 each | NREL NSRDB / PVWatts (task-specified reference sites) | NREL data terms (free, attribution) | Normalized output |
| 10 | `eia930_about.pdf` | PDF | — | EIA | Public domain | Demand definition |
| 11 | `planning_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 12 | `analyst_first_cut.xlsx` | XLSX | 12 | Task author | — | The net-growth figure to correct |

## 5. Deterministic solution path

1. For each hour of 2023–2025: gross = net + BTM capacity(month) × profile(hour).
2. Hour-of-year average gross across the three years; × 1.015.
3. 2026 BTM output = 2026 monthly capacity × average profile(hour-of-year).
4. 2026 net = gross forecast − 2026 BTM output; monthly minima; committed level and binding month.
5. Contrast: growth applied to net; incremental-only subtraction; trend in historical monthly minima.

## 6. Wrong paths (method errors, not misreadings)

**A — grow the net series.** Misses new BTM capacity; minimum too high by roughly the capacity added × midday profile.

**B — subtract only the capacity increment from grown net.** Close but inflates the old BTM part by the growth rate.

**C — extrapolate minima trend 2019–2025.** Assumes pre-2023 adoption pace; minimum too low.

**D — use annual-average profile for all months.** Mis-states spring midday output; wrong binding month.

## 7. Why the stump is analytical, not semantic

The memo states that demand is already net of rooftop solar and gives every input. The wrong answers come from
forecasting the composite series instead of its components — an analytical modelling choice.

## 8. Draft task prompt (prose)

> Set our spring oversupply planning level for 2026: the lowest hourly net load we should expect in any month, following
> the planning memo. Use the EIA-930 load, the rooftop-solar capacity files and the PV profiles in the folder, forecast
> each month's minimum net-load hour for 2026, and tell me the committed level and the month that sets it. Provide
> `monthly_min_net_load_2026.csv` (for each month: minimum net load, its hour, forecast gross consumption and rooftop
> output at that hour, and the 2025 actual minimum), and `duck_curve_2026.png` showing an average April day for 2023, 2025
> and the 2026 forecast, with gross and net lines. Add a one-page `oversupply_memo.pdf` giving the committed level and how
> far the first-cut estimate was off.

## 9. Deliverables

* `monthly_min_net_load_2026.csv`, `duck_curve_2026.png`, `oversupply_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 12 monthly minima (+ their hours) = 24; committed level; binding month; first-cut gap.

## 11. Golden-output checklist

* Gross reconstitution with month-specific capacity; growth on gross only; 2026 BTM subtracted; minima per month.

## 12. Build notes (scope tuning)

* Confirm the NEM interconnection file's capacity units (AC vs DC) and convert consistently; state the convention in the
  memo.
* Check that Trap A's committed level differs by more than 1,000 MW; if not, extend to 2027.
