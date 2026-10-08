# OS46 — Sizing telehealth from 2020: the spike is not the market

| Field | Value |
|---|---|
| Category | Opportunity Sizing |
| Mirrors | Sizing a market from a viral or shock-driven spike (pandemic demand, a product going viral, a competitor outage) where usage decays to a new plateau |
| Domain | Healthcare delivery / digital health |
| Task shape | 02 · Forecast across many periods (quarterly telehealth user share 2024–2026 by beneficiary group; the steady-state level used to size a virtual-care platform) |
| Core method | Quarterly share of beneficiaries using telehealth from 2020 Q1 onward; fit an exponential decay to a plateau, s(t) = s∞ + (s0 − s∞) e^(−kt), from the post-peak period (2020 Q3 onward); steady state s∞ by group; projection; contrast with peak-based and latest-quarter-based sizing |
| Analytical stump | Sizing on the 2020 peak overstates; sizing on the latest quarter may still include decay (or policy-cliff effects). The plateau must be estimated from the decay dynamics, by group, because rural and urban, behavioural and medical services settle at different levels |
| Primary sources | CMS Medicare Telehealth Trends dataset (quarterly telehealth utilisation by beneficiary characteristics) |

## 1. The real-world situation

A virtual-care company sizes its Medicare market. The pitch used the 2020 Q2 share of beneficiaries using telehealth; a revised deck used the
latest quarter. Investors asked for a steady-state estimate with group detail.

## 2. The decision (one deterministic recommendation)

**The steady-state telehealth user share by group (urban/rural × behavioural-health users per memo) and the resulting addressable beneficiaries,
with quarterly projections to 2026.**

Rules (strategy memo):

* Data: CMS Medicare Telehealth Trends, quarterly, national and by urban/rural; measure = percentage of beneficiaries with a telehealth service.
* Fit window: 2020 Q3 to the latest quarter; model s(t) = s∞ + (s0 − s∞) e^(−k t) by nonlinear least squares per group, t in quarters since
  2020 Q3.
* Addressable = s∞ × beneficiaries in the group (memo's counts).
* Projections 2024 Q1–2026 Q4 from the fitted curves.
* Report peak-based and latest-quarter-based sizes for contrast.

## 3. Why capable analysts get it wrong

* Peak values are memorable and large.
* The latest quarter may not have converged.
* Groups converge to different plateaus.
* Policy changes (flexibility extensions) can shift the plateau; the memo fixes the assumption.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `Medicare_Telehealth_Trends.csv` | CSV | ~5k rows (quarter × breakdown) | CMS data.cms.gov | U.S. Gov public domain | Telehealth utilisation |
| 2 | `telehealth_trends_methodology.pdf` | PDF | — | CMS | Public domain | Definitions |
| 3 | `beneficiary_counts.json` | JSON | — | Task author (from CMS enrolment dashboards) | Public domain | Group sizes |
| 4 | `strategy_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `pitch_peak_sizing.xlsx` | XLSX | — | Task author | — | Naive sizing |
| 6 | `fit_starting_values.json` | JSON | — | Task author | — | Optimiser settings |

## 5. Deterministic solution path

1. Extract quarterly shares by group.
2. Fit decay curves; s∞, k per group.
3. Addressable beneficiaries; projections.
4. Contrast with peak and latest-quarter sizing.

## 6. Wrong paths (method errors, not misreadings)

**A — peak sizing.** Overstated.

**B — latest-quarter sizing.** May still be decaying.

**C — single national curve.** Group differences lost.

**D — fitting from 2020 Q1 (pre-spike).** Misfit.

## 7. Why the stump is analytical, not semantic

The model and window are specified. The trap is sizing on transient dynamics instead of a fitted steady state.

## 8. Draft task prompt (prose)

> What is the steady-state Medicare telehealth market we should size against? Fit the decay-to-plateau model by group as the strategy memo
> specifies. Provide `telehealth_projection.csv` (group × quarter: observed, fitted, projected; s∞, k), `decay_curves.png`, and a one-page
> `market_size.pdf`.

## 9. Deliverables

* `telehealth_projection.csv`, `decay_curves.png`, `market_size.pdf`.

## 10. Where 25+ rubric criteria come from

* s∞ and k for 4 groups; addressable counts; 12 projected quarters (sampled); contrasts.

## 11. Golden-output checklist

* Data extraction; fit window; model; starting values; projections; contrast.

## 12. Build notes (scope tuning)

* Confirm peak sizing is ≥ 2× steady state.
