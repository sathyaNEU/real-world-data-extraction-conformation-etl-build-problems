# DS29 — Where to add edge locations: improving the average user is not improving the slow users

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | CDN and edge PoP placement at content and cloud providers, where SLOs are set on latency percentiles |
| Domain | Internet infrastructure |
| Task shape | 01 · Ranked list under a cap (3 new PoP cities chosen from 15 candidates, greedily, by reduction in user-weighted p95 latency) |
| Core method | Latency matrix from measurement probes to candidate city anchors; each user population (probe region weighted by internet users) is served by its lowest-latency PoP; objective = user-weighted 95th percentile of latency; greedy selection adding the city that most reduces p95; compare with selection by mean latency reduction (p-median) |
| Analytical stump | Choosing sites that minimise average latency favours dense regions already well served; the p95 objective targets the tail populations (distant regions, poor peering) that drive SLO breaches. Weighted percentiles must be computed over user-weighted distributions, not over probes |
| Primary sources | RIPE Atlas built-in and anchoring measurements (ping RTTs from probes to anchors) |

## 1. The real-world situation

A CDN will add **3** PoPs among 15 candidate cities to meet a 95th-percentile latency SLO of 60 ms for its users. Network planning ranked candidates
by the reduction in average latency and picked three in Europe and North America. The SLO is breached mostly by users in regions with long paths.

## 2. The decision (one deterministic recommendation)

**The 3 cities selected (greedy, by user-weighted p95 reduction), the p95 after each addition, and whether the SLO is met.**

Rules (planning memo):

* Data: RIPE Atlas anchoring ping measurements (median RTT per probe–anchor pair over the month in memo) from probes to anchors in existing PoP
  cities and the 15 candidate cities.
* Users: probes grouped by country; each country weighted by internet users (memo's table) split equally among its probes with valid data.
* Service: each probe uses the minimum RTT among available PoPs (existing + selected).
* Objective: weighted 95th percentile of probe RTT (memo's weighted quantile definition).
* Greedy: add the candidate with the largest p95 reduction; repeat 3 times; tie → larger user population newly improved.
* Contrast: greedy by weighted mean RTT.

## 3. Why capable analysts get it wrong

* Mean latency is the common optimisation target (p-median).
* SLOs on percentiles depend on the tail population.
* Probe density is uneven; weighting by users is needed.
* Greedy updates must recompute with selected sites included.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `ripe_atlas_anchoring_pings_<month>.jsonl` | JSON lines | ~50–100M results | RIPE Atlas measurement API / daily dumps | RIPE NCC Atlas terms (open data with attribution) | Ping RTTs |
| 2 | `ripe_atlas_probes.json` | JSON | ~12k probes | RIPE Atlas | Same | Probe metadata (country, status) |
| 3 | `ripe_atlas_anchors.json` | JSON | ~800 anchors | RIPE Atlas | Same | Anchor locations |
| 4 | `candidate_cities.json` | JSON | 15 | Task author | — | Candidates and their anchors |
| 5 | `existing_pops.json` | JSON | ~20 | Task author | — | Current PoPs |
| 6 | `internet_users_by_country.csv` | CSV | ~200 | World Bank WDI (internet users) | CC BY 4.0 | Weights |
| 7 | `planning_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 8 | `planning_mean_latency_choice.xlsx` | XLSX | 15 | Task author | — | Naive choice |

## 5. Deterministic solution path

1. Aggregate median RTTs per probe–anchor; map anchors to cities.
2. Compute current served RTTs; weights.
3. Greedy p95 selection; SLO check; mean-based contrast.

## 6. Wrong paths (method errors, not misreadings)

**A — mean-latency greedy.** Ignores tail regions.

**B — unweighted probes.** Europe over-represented.

**C — p95 over probe–anchor pairs instead of served RTTs.** Wrong distribution.

**D — no recomputation after each pick.** Redundant sites.

## 7. Why the stump is analytical, not semantic

The objective, weights and procedure are specified. The trap is optimising the mean when the decision targets a percentile.

## 8. Draft task prompt (prose)

> Which three cities should host new PoPs to meet our p95 latency SLO? Run the user-weighted p95 greedy selection on RIPE Atlas measurements as the
> planning memo specifies. Provide `pop_selection.csv` (round: city, p95 after, mean after), `latency_cdf.png`, and a one-page `pop_expansion.pdf`.

## 9. Deliverables

* `pop_selection.csv`, `latency_cdf.png`, `pop_expansion.pdf`.

## 10. Where 25+ rubric criteria come from

* 3 picks; p95 and mean after each; candidate p95 reductions in round 1 (15); SLO verdict; mean-based contrast.

## 11. Golden-output checklist

* RTT aggregation; weighting; served RTT; weighted quantile; greedy updates.

## 12. Build notes (scope tuning)

* Confirm the mean-based picks differ from p95-based picks by at least two cities.
