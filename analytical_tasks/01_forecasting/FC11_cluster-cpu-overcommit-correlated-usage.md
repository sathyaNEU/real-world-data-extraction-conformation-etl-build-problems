# FC11 — How far can we overcommit CPU? Diversification only works if the tasks don't move together

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Hyperscaler cluster schedulers overcommitting reserved resources (Borg/Kubernetes-style capacity planning) |
| Domain | Cloud infrastructure / capacity planning |
| Task shape | 04 · Setting one dial (machine-level CPU overcommit ratio) |
| Core method | Empirical tail quantile of the **machine-level aggregate** usage-to-limit ratio over 5-minute windows; out-of-sample check on a later week |
| Analytical stump | Per-task usage percentiles combined under an independence (√n) assumption overstate diversification: tasks of the same job and the same diurnal cycle rise together. The tail of the sum must be measured on the sum |
| Primary sources | Google cluster-usage traces v3 (ClusterData 2019) |

## 1. The real-world situation

A cluster team wants to raise the CPU **overcommit ratio** (Σ task CPU limits ÷ machine CPU capacity) for next quarter so more
work fits on the same fleet, while keeping the chance that a machine's actual demand exceeds its capacity in any 5-minute
window at or below 0.1%. The capacity analyst estimated each task's 99.9th-percentile usage-to-limit ratio, then assumed tasks
on a machine are independent and computed the aggregate tail with a normal approximation. The proposed ratio was 2.4×. The
SRE lead noted that most tasks on a machine belong to a handful of jobs that peak at the same hour.

## 2. The decision (one deterministic recommendation)

**The overcommit ratio R to deploy, and the realized exceedance rate it would have produced in the hold-out week.**

Rules (capacity memo):

* Trace: cell `a`, calibration week = days 1–7, hold-out week = days 15–21 of the trace; machines present for the whole week.
* For every machine and 5-minute window: U = Σ over running instances of `average_usage.cpus`; L = Σ of their CPU limits
  (`resource_request.cpus` from the instance events in effect). Windows with L = 0 are skipped.
* q = the 99.9th percentile (inclusive linear interpolation) of U ÷ L over all calibration machine-windows.
* R = 1 ÷ q, rounded down to two decimals. Exceedance in the hold-out week = share of machine-windows where U × R ÷ L > 1
  (i.e. the demand that would land on a machine packed to R would exceed capacity).

## 3. Why capable analysts get it wrong

* Per-task statistics are easy to compute and reuse; aggregate statistics require joining usage to placement window by window.
* The square-root diversification rule holds for independent tasks; replicas of one job and shared traffic cycles create strong
  positive correlation.
* Means (or medians) of utilization suggest overcommit ratios of 4–5×; tails are what break machines.
* Calibrating and evaluating on the same week hides how stable the tail is.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–7 | `instance_usage_a_day01.json.gz` … `day07` | JSON (gz) | 10–30M each | Google ClusterData2019 (BigQuery export) | CC BY 4.0 | 5-minute usage per instance |
| 8–14 | `instance_usage_a_day15.json.gz` … `day21` | JSON (gz) | 10–30M each | Same | CC BY 4.0 | Hold-out week |
| 15 | `instance_events_a_week1_week3.parquet` | Parquet | 20–60M | Same | CC BY 4.0 | Placement and limits |
| 16 | `machine_events_a.csv` | CSV | ~100k | Same | CC BY 4.0 | Machine capacity and availability |
| 17 | `collection_events_a.parquet` | Parquet | ~5M | Same | CC BY 4.0 | Job membership (for correlation diagnostics) |
| 18 | `clusterdata2019_schema.pdf` | PDF | — | Google (trace documentation) | CC BY 4.0 | Field definitions, units |
| 19 | `borg_next_generation_paper.pdf` (citation) | PDF | — | EuroSys 2020 (cite) | Cite | Context |
| 20 | `capacity_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 21 | `analyst_independence_estimate.xlsx` | XLSX | ~50 | Task author | — | The 2.4× proposal |

## 5. Deterministic solution path

1. Build instance-to-machine placement intervals and CPU limits from instance events.
2. Aggregate usage and limits per machine-window in the calibration week; compute U ÷ L; take the 99.9th percentile; R = 1 ÷ q.
3. Apply R to the hold-out week; compute exceedance share.
4. Contrast with the independence estimate and its hold-out exceedance.

## 6. Wrong paths (method errors, not misreadings)

**A — independence/normal aggregation.** Overstates diversification; R too high; hold-out exceedance well above 0.1%.

**B — mean or median utilization.** R absurdly high.

**C — per-task P99.9 summed.** Overly conservative (assumes all peak together); R too low.

**D — calibrate and evaluate on the same week.** No evidence the ratio is safe.

## 7. Why the stump is analytical, not semantic

Usage, limits, windows and the target exceedance are defined. The error is how the tail of a sum is estimated — a probabilistic
modelling choice about dependence, not a reading of the trace.

## 8. Draft task prompt (prose)

> We want to raise CPU overcommit next quarter without letting machine demand exceed capacity in more than 0.1% of 5-minute
> windows. Using the cluster trace and the capacity memo in the folder, calibrate the ratio on the first week and test it on the
> hold-out week. Give me `overcommit_calibration.csv` (the U/L distribution summary: percentiles from 50th to 99.99th, machine-windows
> used), `aggregate_vs_independent.png` comparing the empirical tail of U/L with the independence-based tail, and a one-page
> `overcommit_memo.pdf` with R, the hold-out exceedance it produced, and the exceedance the 2.4× proposal would have produced.

## 9. Deliverables

* `overcommit_calibration.csv`, `aggregate_vs_independent.png`, `overcommit_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* Percentile ladder (≈10 values), q, R, hold-out exceedance, proposal's exceedance, machine-window counts, correlation diagnostic
  (share of usage from the top 3 jobs per machine), chart elements.

## 11. Golden-output checklist

* Placement-correct aggregation; empirical 99.9th percentile; rounding down; hold-out evaluation; independence contrast.

## 12. Build notes (scope tuning)

* Export the needed slices from BigQuery (`google.com:google-cluster-data`) and document the queries; verify field names
  (`average_usage.cpus`, `resource_request.cpus`).
* Confirm the independence method's hold-out exceedance is > 3× the target.
