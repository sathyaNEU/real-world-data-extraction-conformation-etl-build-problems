# FC12 — Serverless cold starts: forecasting the next invocation means modelling the tail of idle gaps

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Function-as-a-service platforms tuning keep-alive to trade cold starts against idle memory (Lambda/Azure Functions class) |
| Domain | Cloud platforms / serverless runtime operations |
| Task shape | 07 · Grid of cells (application frequency class × keep-alive policy → cold-start and idle-memory metrics; best policy per row) |
| Core method | Per-application inter-arrival-time (IAT) histograms from training days, percentile-based keep-alive windows, out-of-sample replay on later days, app-level (not invocation-weighted) outcome distribution |
| Analytical stump | IATs are heavy-tailed and multimodal; windows set from mean IATs or fixed timeouts miss the tail. Invocation-weighted cold-start rates are dominated by chatty apps and hide that most apps suffer; evaluating on the training days overfits the histograms |
| Primary sources | Azure Functions invocation trace 2019 (Azure Public Dataset) |

## 1. The real-world situation

A serverless platform team must choose how long to keep idle function instances in memory. Product complained that customer
apps invoked a few times an hour almost always start cold. The platform's dashboard reported a 2% cold-start rate — computed
over invocations, where a handful of very busy apps dominate. The team proposed raising the fixed timeout from 10 to 60 minutes;
finance worried about idle memory.

## 2. The decision (one deterministic recommendation)

**Which keep-alive policy should each application frequency class use, and what are its cold-start and idle-memory outcomes on
the evaluation days?**

Rules (runtime memo):

* Data: per-minute invocation counts per function (days 1–14) aggregated to the application; app memory from the allocation
  files. Training = days 1–12; evaluation = days 13–14 (continuous timeline across midnight).
* IAT = minutes between consecutive invocation minutes of an app (invocations within the same minute form one arrival).
* Classes by training-period invocation minutes per day: rare (< 10), medium (10–200), frequent (> 200).
* Policies: F10 (fixed 10-minute keep-alive), F60 (fixed 60), H (per-app keep-alive = 99th percentile of training IATs, capped at
  240 minutes; apps with < 10 training IATs use F60).
* Replay on evaluation days: an arrival is cold if the gap since the previous arrival exceeds the window; idle memory =
  Σ idle minutes kept warm × app memory (MB-minutes).
* Per class, adopt the policy minimizing the **75th percentile across apps** of per-app cold-start rate, subject to class idle
  memory ≤ 1.5 × F10's.

## 3. Why capable analysts get it wrong

* Mean IATs are dominated by short bursts; the gaps that cause cold starts live in the tail.
* Invocation-weighted rates measure the experience of busy apps; customers experience their own app.
* Histograms fit on the evaluation days look perfect and are not available in production.
* Treating each day separately breaks gaps that span midnight.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–14 | `invocations_per_function_md.anon.d01.csv` … `d14.csv` | CSV | ~45–50k functions × 1,440 minute columns each | Azure Public Dataset — Azure Functions 2019 | CC BY 4.0 | Invocation counts |
| 15–16 | `app_memory_percentiles.anon.d01.csv`, `…d13.csv` (sample days) | CSV | ~20k each | Same | CC BY 4.0 | Memory per app |
| 17 | `function_durations_percentiles.anon.d01.csv` | CSV | ~45k | Same | CC BY 4.0 | Context |
| 18 | `azurefunctions_dataset2019_readme.pdf` | PDF | — | Azure Public Dataset | CC BY 4.0 | Schema |
| 19 | `serverless_in_the_wild_atc2020.pdf` (citation) | PDF | — | USENIX ATC 2020 (cite) | Cite | Policy background |
| 20 | `runtime_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 21 | `platform_dashboard_coldstart.xlsx` | XLSX | ~30 | Task author | — | Invocation-weighted metrics |

## 5. Deterministic solution path

1. Aggregate functions to apps; build a continuous minute timeline per app; derive arrivals and IATs.
2. Classify apps; compute H windows from training IATs.
3. Replay F10, F60, H on evaluation days per app: cold-start rate and idle MB-minutes.
4. Per class: 75th percentile of per-app cold-start rate, class idle memory; apply the constraint; adopt.
5. Contrast invocation-weighted rates and mean-IAT windows.

## 6. Wrong paths (method errors, not misreadings)

**A — invocation-weighted cold-start rate.** All policies look fine; F10 retained everywhere.

**B — mean-IAT windows.** Rare/medium apps still start cold.

**C — fit and evaluate on the same days.** H looks better than it is.

**D — per-day timelines.** Midnight gaps miscounted.

## 7. Why the stump is analytical, not semantic

Arrivals, classes, policies and the objective are defined. The traps are distributional (tails vs means), aggregation
(app- vs invocation-weighting) and validation design.

## 8. Draft task prompt (prose)

> Pick the keep-alive policy for each class of application from the runtime memo: the one that minimizes the 75th-percentile
> app's cold-start rate on the last two days without blowing the idle-memory budget, using the Azure Functions trace in the
> folder. Provide `policy_grid.csv` (class × policy: apps, 75th-percentile cold-start rate, median cold-start rate, idle
> MB-minutes, feasible, adopted) and `coldstart_cdf.png` showing per-app cold-start-rate distributions by policy for the medium
> class. Add a one-page `keepalive_memo.pdf` with the adopted policies and why the dashboard's 2% figure was misleading.

## 9. Deliverables

* `policy_grid.csv`, `coldstart_cdf.png`, `keepalive_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 3 classes × 3 policies × (P75 rate, idle memory, feasibility) = 27 cells; adopted policy per class; dashboard contrast.

## 11. Golden-output checklist

* App aggregation; continuous timeline; correct IAT definition; training/evaluation split; app-level P75; constraint applied.

## 12. Build notes (scope tuning)

* Verify file naming and column layout of the 2019 release; publish the app-level aggregation used.
* Confirm the H policy is adopted in at least one class and that invocation weighting would retain F10 everywhere.
