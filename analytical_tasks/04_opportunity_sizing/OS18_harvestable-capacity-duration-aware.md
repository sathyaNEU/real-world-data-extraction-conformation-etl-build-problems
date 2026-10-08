# OS18 — Selling idle capacity: average idle cores are not cores you can promise for six hours

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Harvest and spot-VM products at cloud providers, batch scheduling on idle capacity, ride-hail "idle driver" monetisation |
| Domain | Cloud infrastructure |
| Task shape | 04 · Setting one dial (the number of guaranteed cores sold as a 6-hour batch product) |
| Core method | For each start time, harvestable cores = minimum over the next 6 hours of (allocated cores − used cores) aggregated across VMs on the same hosts per memo; the dial = the largest core count available for ≥ 95% of start times; comparison with mean idle cores |
| Analytical stump | Average idle capacity counts cores idle at different times; a batch job needs the same cores for its whole duration. Idle capacity is correlated across VMs (daily peaks), so the guaranteed level over a window is far below the mean. Sizing on the average oversells and triggers evictions |
| Primary sources | GWA-T-12 Bitbrains VM performance traces (Delft Grid Workloads Archive) |

## 1. The real-world situation

A hosting provider plans to sell a "batch lane": customers get N cores for 6-hour jobs on otherwise idle capacity. The product manager
sized N as the average number of idle cores across the fleet. Operations warned that idle capacity disappears every weekday morning.

## 2. The decision (one deterministic recommendation)

**N, the guaranteed core count for 6-hour jobs available at ≥ 95% of hourly start times over the trace, and the revenue difference versus the
average-based plan.**

Rules (product memo):

* Data: Bitbrains fastStorage and Rnd VM traces (5-minute samples of provisioned cores, CPU usage %), one month.
* Used cores per VM = provisioned cores × CPU usage ÷ 100; idle = provisioned − used.
* Fleet idle at time t = Σ idle across VMs; headroom reserve = 20% of provisioned cores (not sellable).
* Sellable(t) = max(0, fleet idle(t) − reserve).
* Window availability for a start at t = min over t…t+6h of sellable.
* N = 5th percentile (over hourly start times) of window availability, rounded down to a multiple of 8.
* Revenue: price per core-hour × N × 6 × number of jobs per day (memo); compare with the PM's plan at mean sellable.

## 3. Why capable analysts get it wrong

* Average idle is the obvious capacity metric.
* Jobs need continuous availability; minima over windows matter.
* Correlated demand across VMs makes aggregate idle swing together.
* Headroom must be kept for the primary tenants.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `fastStorage/2013-8/<vm>.csv` (1,250 VMs) | CSV (semicolon) | ~8.6k each | GWA-T-12 Bitbrains (Grid Workloads Archive, TU Delft) | Free for research use (archive terms; cite) | VM performance |
| 2 | `Rnd/2013-7..9/<vm>.csv` (500 VMs) | CSV | ~8.6k each | Same | Same | VM performance |
| 3 | `gwa_t12_description.pdf` | PDF | — | Shen et al., CCGrid 2015 (cite) | Cite | Trace description |
| 4 | `product_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `pm_average_sizing.xlsx` | XLSX | — | Task author | — | Naive sizing |
| 6 | `fleet_idle_5min.parquet` | Parquet | ~8.6k | Derived | Same | Aggregated idle |
| 7 | `pricing.json` | JSON | — | Task author | — | Price and job assumptions |
| 8 | `window_min_check.json` | JSON | — | Task author | — | Check values |

## 5. Deterministic solution path

1. Load traces; compute used and idle per VM; align timestamps.
2. Fleet idle; reserve; sellable.
3. Rolling 6-hour minima at hourly starts; 5th percentile; N.
4. Revenue comparison with the average-based plan.

## 6. Wrong paths (method errors, not misreadings)

**A — mean idle.** Oversells.

**B — percentile of instantaneous sellable (no window).** Ignores duration.

**C — per-VM minima summed.** Too conservative (ignores reassignment allowed by memo's fleet pooling).

**D — no reserve.** Violates the memo.

## 7. Why the stump is analytical, not semantic

Definitions and the percentile rule are specified. The trap is ignoring persistence and correlation of idle capacity.

## 8. Draft task prompt (prose)

> How many cores can we guarantee in the 6-hour batch lane? Compute window-based availability from the Bitbrains traces as the product memo
> specifies. Provide `availability_curve.csv` (cores: share of start times available), `idle_profile.png` (fleet sellable over the month with
> the chosen N), and a one-page `batch_lane_sizing.pdf`.

## 9. Deliverables

* `availability_curve.csv`, `idle_profile.png`, `batch_lane_sizing.pdf`.

## 10. Where 25+ rubric criteria come from

* N; availability at 10 core levels; mean sellable; revenue comparison; hourly pattern values.

## 11. Golden-output checklist

* Used-core formula; reserve; window minima; percentile; rounding.

## 12. Build notes (scope tuning)

* Confirm N is below 50% of mean sellable.
