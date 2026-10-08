# DS20 — When to raise the flood wall: one sea-level projection is not a plan

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Infrastructure and capacity decisions under deep uncertainty (data-centre capacity under demand scenarios, network upgrades under adoption scenarios) where waiting has option value |
| Domain | Coastal infrastructure / climate adaptation |
| Task shape | 13 · Scenarios and the flip point (adaptation strategy × sea-level scenario → 50-year cost; the strategy with minimum maximum regret and the scenario at which the choice flips) |
| Core method | High-tide flooding frequency as a function of local relative sea level from tide-gauge records (exceedance of the facility's flood threshold); project exceedance days per year under the 2022 interagency sea-level scenarios; expected damage costs by year; strategies (build now high, build now low + upgrade later, adaptive trigger); regret = cost − best cost per scenario; choose minimax regret |
| Analytical stump | Choosing based on the intermediate scenario's expected cost ignores that the decision is irreversible and scenarios are deeply uncertain; adaptive strategies with triggers preserve flexibility. Converting sea-level rise to flood days must use the local distribution of high water (exceedance curve), not linear extrapolation of past flood counts |
| Primary sources | NOAA CO-OPS tide gauge water levels (hourly/high-low) and high tide flooding thresholds; 2022 U.S. interagency sea level rise scenarios (local projections) |

## 1. The real-world situation

A port authority must protect a coastal facility. The engineering consultant recommended a 1.0 m wall now, sized for the intermediate scenario
in 2075. Finance proposed a 0.5 m wall now with a 0.5 m upgrade when annual flood days exceed a trigger. The board wants a defensible choice
across scenarios.

## 2. The decision (one deterministic recommendation)

**The strategy (from the memo's four) with minimum maximum regret over the five scenarios, its regret table, and the scenario at which the
expected-cost-optimal strategy changes.**

Rules (adaptation memo):

* Gauge: the station in memo; hourly water levels 1990–2023 relative to the station datum; facility threshold (memo) above MHHW.
* Distribution: daily maximum water level anomalies (detrended by the annual mean sea level) — empirical exceedance curve.
* Projection: for each year 2025–2075 and scenario (Low, Intermediate-Low, Intermediate, Intermediate-High, High), shift the distribution by the
  scenario's local SLR; flood days = days with daily max > threshold (+ wall height when protected).
* Costs: damage per flood day; wall costs (memo); upgrade cost and lead time; discount rate 3%.
* Strategies: S1 no wall; S2 1.0 m now; S3 0.5 m now; S4 0.5 m now + 0.5 m upgrade triggered when unprotected-equivalent flood days ≥ 5 per year.
* Regret per scenario = PV cost − min PV cost across strategies; choose minimax regret; flip point for expected-cost choice across scenarios.

## 3. Why capable analysts get it wrong

* Single-scenario design is common.
* Flood frequency responds nonlinearly to sea level through the exceedance curve.
* Irreversible investments under uncertainty favour flexible strategies.
* Discounting and lead times affect adaptive strategies.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `coops_<station>_hourly_1990_2023.csv` | CSV | ~300k | NOAA CO-OPS API | U.S. Gov public domain | Hourly water levels |
| 2 | `coops_<station>_datums.json` | JSON | — | NOAA CO-OPS | Public domain | Datums, MHHW |
| 3 | `htf_thresholds.csv` | CSV | ~100 stations | NOAA (high tide flooding thresholds) | Public domain | Thresholds |
| 4 | `sweet_2022_slr_scenarios_<station>.csv` | CSV | ~5 × 15 decades | NOAA/interagency 2022 technical report data | Public domain | Local projections |
| 5 | `adaptation_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 6 | `consultant_intermediate_design.xlsx` | XLSX | — | Task author | — | Single-scenario design |
| 7 | `cost_assumptions.json` | JSON | — | Task author | — | Costs |
| 8 | `minimax_regret_reference.pdf` | PDF | — | Cite (decision-making under deep uncertainty) | Cite | Method |

## 5. Deterministic solution path

1. Build daily maxima; detrend; exceedance curve.
2. Annual flood days by scenario and wall height; costs; trigger logic.
3. PV costs; regrets; minimax choice; flip point.
4. Contrast with the consultant's single-scenario choice.

## 6. Wrong paths (method errors, not misreadings)

**A — intermediate scenario only.** Ignores regret elsewhere.

**B — linear extrapolation of flood counts.** Misses acceleration.

**C — no detrending.** Double counts sea-level rise.

**D — no lead time for upgrades.** Overvalues adaptive strategy.

## 7. Why the stump is analytical, not semantic

The data, scenarios and criterion are specified. The trap is single-scenario optimisation of an irreversible decision.

## 8. Draft task prompt (prose)

> Which flood-protection strategy should the port adopt? Project flood days under each sea-level scenario from the tide-gauge record and choose by
> minimax regret as the adaptation memo specifies. Provide `regret_table.csv` (strategy × scenario: PV cost, regret), `flood_days_projection.png`, and a
> one-page `adaptation_strategy.pdf`.

## 9. Deliverables

* `regret_table.csv`, `flood_days_projection.png`, `adaptation_strategy.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 strategies × 5 scenarios = 20 PV costs and regrets; choice; flip point; trigger year by scenario.

## 11. Golden-output checklist

* Datum handling; detrending; exceedance shift; trigger; discounting; regret.

## 12. Build notes (scope tuning)

* Confirm the adaptive strategy has minimum maximum regret while S2 wins under the intermediate scenario alone.
