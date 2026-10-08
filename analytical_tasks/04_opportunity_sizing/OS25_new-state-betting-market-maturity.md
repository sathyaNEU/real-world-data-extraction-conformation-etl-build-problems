# OS25 — Sizing a new state's betting market: launch-month handle is inflated by promotions and novelty

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | New-geography launch sizing for consumer platforms (ride-hail, delivery, fintech) using early markets as comparables while those markets were still ramping and promotion-heavy |
| Domain | Gaming / consumer markets |
| Task shape | 02 · Forecast across many periods (monthly gross gaming revenue for the first 24 months in a newly legal state; the year-2 tax revenue the state budgets) |
| Core method | Comparable states' monthly GGR per adult indexed by months since launch (event time), net of promotional credits where reported, seasonally adjusted by calendar month factors (football season); mature level = months 13–24 average; apply to the new state's adult population with the memo's adjustment for mobile-only versus retail mix |
| Analytical stump | Comparing per-capita handle across states at the same calendar month mixes states at different maturity; launch months include promotional credits that inflate handle and depress taxable revenue; football seasonality dominates month-to-month swings. Event-time alignment and promotion netting change the year-2 estimate materially |
| Primary sources | State gaming regulator monthly sports wagering reports (e.g., Pennsylvania Gaming Control Board, New Jersey DGE, Michigan Gaming Control Board, Illinois Gaming Board) |

## 1. The real-world situation

A state budget office must budget year-2 sports-betting tax revenue for a newly legal market. The consultant multiplied the population by
per-adult handle from mature states' latest month and applied the hold rate. The budget office asked for an event-time forecast that nets out
promotional credits and seasonality.

## 2. The decision (one deterministic recommendation)

**Year-2 (months 13–24) taxable GGR and tax revenue for the new state, with the monthly forecast for months 1–24.**

Rules (budget memo):

* Comparables: 4 states with monthly reports covering ≥ 30 months since launch; online sports wagering only.
* Measures: handle, GGR (gross revenue), promotional deductions (where reported), taxable GGR (as defined per state; harmonised per memo).
* Per adult (21+) using Census population estimates by state-year.
* Event time m = months since the state's first full month of mobile wagering.
* Seasonal factors: ratio of each calendar month's taxable GGR to the 12-month centred average, averaged across comparables after month 12.
* Curve: median across comparables of seasonally adjusted taxable GGR per adult at each m (1–24).
* Forecast for the new state = curve(m) × adults × seasonal factor(calendar month of m).
* Tax = taxable GGR × statutory rate (memo).

## 3. Why capable analysts get it wrong

* Latest-month per-capita figures from mature states are easy comparables.
* Markets ramp over 12–18 months; launch-month comparisons understate or overstate depending on alignment.
* Promotions can make taxable revenue near zero in early months.
* Football seasonality creates large monthly swings.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–4 | `<state>_sports_wagering_monthly_reports.xlsx` (4 states) | XLSX | ~40–70 months each, operator rows | State gaming regulators | Public records | Handle, GGR, promotions, tax |
| 5 | `sc-est<yyyy>-agesex-civ.csv` | CSV | ~10k | Census population estimates | Public domain | Adults 21+ |
| 6 | `state_definitions_map.json` | JSON | — | Task author | — | Harmonising taxable GGR definitions |
| 7 | `budget_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 8 | `consultant_estimate.xlsx` | XLSX | — | Task author | — | Naive sizing |
| 9 | `launch_dates.json` | JSON | 5 | Task author | — | Event-time anchors |
| 10 | `new_state_profile.json` | JSON | — | Task author | — | Population, tax rate, launch month |

## 5. Deterministic solution path

1. Harmonise comparables' monthly measures; per-adult conversion.
2. Event-time alignment; seasonal factors; median curve.
3. New-state monthly forecast; year-2 totals and tax.
4. Contrast with the consultant's estimate.

## 6. Wrong paths (method errors, not misreadings)

**A — latest-month mature per-capita.** Ignores ramp and season.

**B — handle × hold without promotion netting.** Overstated taxable revenue.

**C — calendar-month alignment.** Mixes maturity.

**D — total population instead of adults 21+.** Scale error.

## 7. Why the stump is analytical, not semantic

The measures and alignment are specified. The trap is maturity and seasonality in comparables.

## 8. Draft task prompt (prose)

> What sports-betting tax revenue should we budget for year 2? Build the event-time, seasonally adjusted forecast from comparable states as the
> budget memo specifies. Provide `monthly_forecast.csv` (month 1–24: per-adult curve, seasonal factor, taxable GGR, tax), `ramp_curves.png`, and a
> one-page `budget_estimate.pdf`.

## 9. Deliverables

* `monthly_forecast.csv`, `ramp_curves.png`, `budget_estimate.pdf`.

## 10. Where 25+ rubric criteria come from

* 24 monthly forecasts; year-2 totals; seasonal factors (12); contrast.

## 11. Golden-output checklist

* Harmonisation; per-adult; event time; seasonal factors; median curve; tax.

## 12. Build notes (scope tuning)

* Confirm the consultant's estimate exceeds the event-time year-2 figure by ≥ 25%.
