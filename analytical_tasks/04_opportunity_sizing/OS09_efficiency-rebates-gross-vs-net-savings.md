# OS09 — Rebate programme savings: customers who would have bought anyway are not savings

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Promotion and incentive sizing (coupons, cashback, sales incentives) where many recipients would have purchased without the incentive |
| Domain | Utility energy-efficiency programmes |
| Task shape | 03 · Bridge between two totals (programme portfolio gross savings → net savings after free-ridership and spillover; the programme expanded next cycle) |
| Core method | Net savings = gross savings × net-to-gross ratio (NTG = 1 − free-ridership + spillover) by programme and measure group, using evaluated NTG values from the claims data; cost per net kWh; ranking programmes by net savings per dollar |
| Analytical stump | Gross reported savings credit every rebated purchase; high-efficiency products with strong market adoption (LED lighting, efficient appliances) have high free-ridership. Ranking by gross cost-effectiveness favours programmes with the most free riders |
| Primary sources | California Public Utilities Commission CEDARS (California Energy Data and Reporting System) public claims data |

## 1. The real-world situation

A utility's portfolio planner will expand one residential programme next cycle based on cost per kWh saved. The plan ranked programmes by
gross first-year savings per programme dollar and recommended a lighting-heavy programme. The regulator's evaluators publish net-to-gross
ratios showing that many of those customers would have bought LEDs anyway.

## 2. The decision (one deterministic recommendation)

**The residential programme expanded: lowest programme cost per *net* first-year kWh among programmes with ≥ 5 GWh gross savings, and the
portfolio bridge from gross to net.**

Rules (portfolio memo):

* Data: CEDARS claims for the utility and program year in the memo; residential sector programmes.
* Gross savings: first-year kWh (`NumUnits × UnitkWh1stBaseline` or the claims field per memo, including realisation rate where applied).
* NTG: claim-level `NTG_ELEC` (ex-ante values as reported); net = gross × NTG.
* Programme cost: total programme expenditure from the program-level cost file.
* Eligible: gross ≥ 5 GWh.
* Choose the lowest cost ÷ net kWh. Bridge: Σ gross → free-ridership adjustment → spillover → Σ net (by measure group).

## 3. Why capable analysts get it wrong

* Gross savings are what programmes report first.
* Free-ridership varies widely by measure; it is the key correction.
* NTG must be applied at claim/measure level before aggregating.
* Cost-effectiveness rankings change when denominators change.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `cedars_claims_<utility>_<year>.csv` | CSV | ~100k–500k claims | CPUC CEDARS public data | Public (California public records) | Claims with savings and NTG |
| 2 | `cedars_program_costs_<year>.csv` | CSV | ~300 | CPUC CEDARS | Public | Programme costs |
| 3 | `cedars_field_definitions.pdf` | PDF | — | CPUC | Public | Field definitions |
| 4 | `measure_group_map.json` | JSON | ~50 | Task author | — | Measure grouping |
| 5 | `portfolio_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `planner_gross_ranking.xlsx` | XLSX | ~20 | Task author | — | Gross ranking |
| 7 | `cpuc_ntg_evaluation_citation.pdf` | PDF | — | CPUC evaluation reports (cite) | Public | NTG basis |
| 8 | `deer_measure_reference.csv` | CSV | ~5k | DEER (California) | Public | Context |

## 5. Deterministic solution path

1. Filter utility, year, residential programmes; compute gross and net per claim.
2. Aggregate by programme; join costs; eligibility.
3. Cost per net kWh; choose; bridge.
4. Contrast with gross ranking.

## 6. Wrong paths (method errors, not misreadings)

**A — gross cost-effectiveness.** Free-rider-heavy programme chosen.

**B — portfolio-average NTG.** Measure differences lost.

**C — lifecycle versus first-year mix.** Not the memo's basis.

**D — ignoring programme costs not tied to claims.** Understated cost.

## 7. Why the stump is analytical, not semantic

Fields and formulas are specified. The trap is attributing all observed purchases to the incentive.

## 8. Draft task prompt (prose)

> Which residential programme should we expand? Rank programmes by cost per net kWh as the portfolio memo defines it, and bridge the portfolio
> from gross to net savings. Provide `programme_net_savings.csv` (programme: gross, NTG, net, cost, cost per net kWh), `gross_to_net_bridge.png`,
> and a one-page `expansion_choice.pdf`.

## 9. Deliverables

* `programme_net_savings.csv`, `gross_to_net_bridge.png`, `expansion_choice.pdf`.

## 10. Where 25+ rubric criteria come from

* Eligible programmes' gross, net, cost per net kWh (≈ 8 × 3); bridge by measure group; choice; contrast.

## 11. Golden-output checklist

* Filters; claim-level NTG; aggregation; costs; eligibility; bridge.

## 12. Build notes (scope tuning)

* Confirm the gross leader is not the net leader.
