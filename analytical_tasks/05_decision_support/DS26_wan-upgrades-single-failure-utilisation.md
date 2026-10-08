# DS26 — Which backbone links to upgrade? Size for the day a neighbouring link fails

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | WAN and data-centre network capacity planning at network vendors and cloud providers (N−1 resilience planning) |
| Domain | Telecommunications / network engineering |
| Task shape | 01 · Ranked list under a cap (8 links upgraded this budget cycle, ranked by worst-case utilisation under single-link failures) |
| Core method | Route the measured traffic matrices on the topology with shortest-path (IGP weights) routing; compute link loads in the normal state and under every single-link failure (rerouting); worst-case utilisation per link = max over failure scenarios of load ÷ capacity at the 95th-percentile traffic matrix; upgrade links whose worst case exceeds 90%, highest first |
| Analytical stump | Upgrading links whose normal-state peak utilisation is highest misses links that are lightly loaded normally but absorb large flows when a parallel path fails. Planning on normal utilisation leaves the network unable to survive single failures; failure-scenario routing changes the upgrade list |
| Primary sources | GÉANT traffic matrices dataset (TOTEM project, 15-minute matrices) and GÉANT topology with link capacities and IGP weights |

## 1. The real-world situation

A research and education network can upgrade **8** backbone links this year. Engineering's draft upgrades the eight links with the highest
95th-percentile normal-state utilisation. The resilience policy requires that no link exceed 90% utilisation under any single-link failure.

## 2. The decision (one deterministic recommendation)

**The 8 links upgraded (ranked by worst-case single-failure utilisation above 90%), the 9th, and the links on the draft list that the resilience
criterion does not require.**

Rules (planning memo):

* Data: GÉANT 15-minute traffic matrices (4 months in memo); topology with link capacities and IGP weights (the dataset's topology file).
* Planning matrix: per origin–destination pair, the 95th percentile over the period (memo convention), scaled by 1.3 for growth.
* Routing: shortest paths by IGP weight with ECMP equal splitting; failures: remove one link at a time (both directions), recompute routes.
* Utilisation: load ÷ capacity per direction; worst case = max over normal and all single-link failure states.
* Candidates: links with worst case > 90%; rank by worst case; top 8; report #9.
* Draft contrast: top 8 by normal-state utilisation.

## 3. Why capable analysts get it wrong

* Normal-state utilisation dashboards are the daily view.
* Failures reroute traffic onto other links, sometimes doubling load.
* ECMP and IGP weights determine where traffic shifts.
* Per-pair 95th percentiles across the matrix overstate simultaneous peaks (memo's convention accepted).

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `geant_traffic_matrices/IntraTM-<date>.xml` | XML | ~10k matrices × 23×23 pairs | TOTEM GÉANT dataset (Uhlig et al.) | Public research dataset (cite; verify terms) | Traffic matrices |
| 2 | `geant_topology.xml` | XML | ~38 links | Same | Same | Nodes, links, capacities, IGP weights |
| 3 | `uhlig_2006_citation.pdf` | PDF | — | Uhlig et al., CCR 2006 (cite) | Cite | Dataset description |
| 4 | `planning_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `draft_normal_utilisation_list.xlsx` | XLSX | ~38 | Task author | — | Draft list |
| 6 | `routing_check_cases.json` | JSON | — | Task author | — | Hand-checked routes |
| 7 | `planning_matrix.csv` | CSV | ~500 pairs | Derived | Same | 95th-percentile matrix |

## 5. Deterministic solution path

1. Parse matrices and topology; compute the planning matrix.
2. Route normally and under each single-link failure with ECMP.
3. Utilisation per link and state; worst cases; ranking; top 8.
4. Contrast with the draft list.

## 6. Wrong paths (method errors, not misreadings)

**A — normal-state utilisation ranking.** Misses failure hotspots.

**B — failures without ECMP splitting.** Wrong loads.

**C — mean traffic matrix.** Understates peaks.

**D — ignoring direction.** Asymmetric loads missed.

## 7. Why the stump is analytical, not semantic

Routing, scenarios and thresholds are specified. The trap is planning for normal operation rather than the resilience requirement.

## 8. Draft task prompt (prose)

> Which eight backbone links should we upgrade to meet the single-failure policy? Route the planning traffic matrix under all single-link failures as the
> planning memo specifies. Provide `link_worst_case.csv` (link: normal utilisation, worst-case utilisation, failing link causing it, rank),
> `failure_heatmap.png`, and a one-page `upgrade_plan.pdf`.

## 9. Deliverables

* `link_worst_case.csv`, `failure_heatmap.png`, `upgrade_plan.pdf`.

## 10. Where 25+ rubric criteria come from

* 8 links + #9; worst-case values and causing failures for 10 links; draft contrast; routing checks.

## 11. Golden-output checklist

* Matrix construction; ECMP; failure enumeration; utilisation; ranking.

## 12. Build notes (scope tuning)

* Confirm at least three draft links are not needed and three non-draft links exceed 90% under failures.
