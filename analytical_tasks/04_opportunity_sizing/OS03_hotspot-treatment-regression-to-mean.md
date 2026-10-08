# OS03 — Treating the worst intersections: last year's crash counts overstate next year's benefit

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Targeting programmes aimed at extreme units (top-decile churn-risk users, highest-cost patients, most-complained-about stores) whose outcomes partly revert on their own |
| Domain | Road safety / city operations |
| Task shape | 03 · Bridge between two totals (naive crashes avoided at the 50 selected intersections → empirical-Bayes expected crashes avoided; the budget request) |
| Core method | Safety performance function (negative binomial regression of injury crashes on traffic proxies and intersection type) fitted on all intersections; empirical-Bayes expected crashes for each selected site = w × SPF prediction + (1 − w) × observed, w = 1 ÷ (1 + μ/φ); benefit = crash modification factor applied to the EB expectation |
| Analytical stump | Sites are selected *because* they had many crashes in the selection period; part of that excess is chance and will not recur. Applying the treatment's crash reduction to observed counts overstates the benefit; the EB expectation removes regression to the mean |
| Primary sources | NYC Motor Vehicle Collisions — Crashes (NYC Open Data); NYC street centerline (LION) intersections; NYC DOT traffic volume counts |

## 1. The real-world situation

A city transportation department will redesign the **50** intersections with the most injury crashes over 2021–2023. The budget request sizes
the benefit as 30% (the treatment's crash modification factor) of those 50 intersections' observed crashes. A safety engineer warned that
high-crash sites tend to have fewer crashes the following years even without treatment.

## 2. The decision (one deterministic recommendation)

**The expected injury crashes avoided per year at the 50 sites using EB expectations, the bridge from the naive figure, and whether the
programme meets the memo's cost-effectiveness threshold.**

Rules (safety memo):

* Crashes: injury crashes (persons injured or killed ≥ 1) geocoded within 30 m of an intersection node, 2021–2023 (selection period).
* Intersections: nodes with ≥ 3 legs; type by legs and signal status (provided).
* SPF: negative binomial regression of 3-year injury crashes on log(entering volume proxy), number of legs, signalised flag; fitted on all
  intersections; dispersion φ.
* Selection: top 50 by observed 3-year injury crashes (ties by fatalities).
* EB expected per year = [w × μ + (1 − w) × observed] ÷ 3 with w = 1 ÷ (1 + μ ÷ φ) (memo's parameterisation).
* Avoided per year = 0.30 × EB expected (CMF 0.70).
* Cost-effectiveness: programme cost ÷ avoided crashes per year ≤ $400,000 (memo).
* Naive: 0.30 × observed ÷ 3.

## 3. Why capable analysts get it wrong

* Observed counts are the obvious baseline.
* Selection on extreme values guarantees some reversion.
* The SPF captures what an intersection "like this" typically experiences.
* Validation: the selected sites' 2024 crashes (if available) fall toward EB expectations (memo includes for checking only).

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `Motor_Vehicle_Collisions_-_Crashes.csv` | CSV | ~2.1M | NYC Open Data | NYC Open Data terms (open) | Crashes with coordinates, injuries |
| 2 | `lion_nodes.geojson` | GeoJSON | ~150k | NYC Department of City Planning (LION) | Open | Intersection nodes, legs |
| 3 | `signalized_intersections.csv` | CSV | ~13k | NYC DOT open data | Open | Signal status |
| 4 | `Automated_Traffic_Volume_Counts.csv` | CSV | ~30M | NYC Open Data (DOT) | Open | Volume proxy |
| 5 | `volume_proxy_by_node.parquet` | Parquet | ~45k | Derived per memo | Open | Entering volume proxy |
| 6 | `safety_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `budget_request_naive.xlsx` | XLSX | 50 | Task author | — | Naive sizing |
| 8 | `hauer_eb_method_citation.pdf` | PDF | — | Hauer; AASHTO Highway Safety Manual (cite) | Cite | EB method |
| 9 | `programme_cost.json` | JSON | — | Task author | — | Cost |

## 5. Deterministic solution path

1. Snap crashes to intersections; count injury crashes per node.
2. Fit the SPF; compute μ, φ.
3. Select 50; EB expectations; avoided crashes; bridge; cost-effectiveness.
4. Validation against 2024 observed (context).

## 6. Wrong paths (method errors, not misreadings)

**A — naive observed-based benefit.** Overstated.

**B — SPF prediction alone.** Ignores site-specific information.

**C — Poisson SPF.** Wrong weights (no overdispersion).

**D — selecting and estimating on the same crashes without EB.** Circular.

## 7. Why the stump is analytical, not semantic

Snapping, SPF and EB formulas are specified. The trap is regression to the mean from selection on extremes.

## 8. Draft task prompt (prose)

> How many injury crashes will redesigning our 50 worst intersections actually avoid each year? Use the empirical-Bayes method in the safety
> memo and bridge from the budget request's figure. Provide `site_expectations.csv` (site: observed, SPF, weight, EB, avoided), `rtm_bridge.png`,
> and a one-page `programme_benefit.pdf` with the cost-effectiveness call.

## 9. Deliverables

* `site_expectations.csv`, `rtm_bridge.png`, `programme_benefit.pdf`.

## 10. Where 25+ rubric criteria come from

* SPF coefficients and φ; EB values for 10 sites; totals naive and EB; bridge; decision.

## 11. Golden-output checklist

* Snapping radius; injury filter; SPF; EB weight; CMF; cost threshold.

## 12. Build notes (scope tuning)

* Confirm naive ÷ EB ≥ 1.4 and that the cost-effectiveness call flips.
