# FC45 — Booking reserves from shale-well decline curves: hyperbolic declines need a floor

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Upstream oil & gas reserve estimation and type curves (reserve write-downs after over-optimistic decline assumptions) |
| Domain | Energy / petroleum engineering / capital allocation |
| Task shape | 14 · Cuts of a distribution (P90/P50/P10 EUR across wells for the type curve) |
| Core method | Per-well modified hyperbolic decline (Arps hyperbolic switching to exponential at a terminal decline rate), fitted on rate per producing day by grid search; EUR = cumulative + forecast to 30 years; exceedance percentiles across wells |
| Analytical stump | Shale wells fit hyperbolic exponents b > 1, for which cumulative production never converges — EURs balloon unless a terminal decline is imposed. Exponential fits to early transient data under-state; fitting monthly volumes without normalizing for producing days reads downtime as decline |
| Primary sources | Pennsylvania DEP oil & gas production reports (well-level), PA DEP well inventory |

## 1. The real-world situation

An operator's reservoir team must publish a **type curve** (P90/P50/P10 estimated ultimate recovery, EUR) for its Marcellus acreage to
justify next year's drilling budget. The analyst fitted unconstrained hyperbolic declines to each well and reported a P50 EUR well above
what offset operators were booking. The reserves auditor asked what terminal decline had been assumed.

## 2. The decision (one deterministic recommendation)

**The type curve: P90, P50 and P10 EUR (Bcf) across the analysis wells, where P90 is the value exceeded by 90% of wells.**

Rules (reserves memo):

* Wells: unconventional gas wells in the counties listed, first production 2014–2019, ≥ 36 months of production reported.
* Rate: monthly gas volume ÷ producing days (Mcf/d); months with < 15 producing days excluded from fitting.
* Model: q(t) = q_i / (1 + b·D_i·t)^(1/b), switching to exponential decline when the instantaneous decline falls to D_min = 6% per
  year (effective). Grid search over b ∈ {0.1, 0.2, …, 2.0} and D_i on a 0.5%-per-month grid, minimizing SSE of ln(q) over months
  after peak.
* EUR = cumulative to date + forecast from the last month to 30 years after first production (no economic limit).
* Percentiles across wells with the exceedance convention: P90 = 10th percentile of EUR, P10 = 90th percentile (inclusive
  interpolation).

## 3. Why capable analysts get it wrong

* Unconstrained hyperbolic fits on shale wells routinely return b > 1, where the integral to infinity diverges.
* Early months are in transient flow; exponential fits on them are too steep.
* Downtime (shut-ins, pad drilling) appears as dips in monthly volumes; rate per producing day removes it.
* Reserve percentile conventions are reversed relative to ordinary percentiles.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–9 | `OilGasProduction_YYYY.csv` (2015–2023, unconventional) | CSV | 100k–150k each | Pennsylvania DEP Office of Oil & Gas Management | Commonwealth of PA public data | Well-month production and producing days |
| 10 | `OilGasProduction_2010_2014_semiannual.csv` | CSV | ~100k | PA DEP | Same | Early history |
| 11 | `well_inventory.csv` | CSV | ~200k | PA DEP | Same | Well type, county, spud dates |
| 12 | `production_reporting_guidance.pdf` | PDF | — | PA DEP | Same | Field definitions |
| 13 | `spe_prms_2018_excerpt.pdf` (citation) | PDF | — | SPE-PRMS (cite) | Cite | Reserves percentile convention |
| 14 | `arps_modified_hyperbolic_reference.pdf` (citation) | PDF | — | Cite | Cite | Decline model |
| 15 | `reserves_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 16 | `analyst_unconstrained_fits.xlsx` | XLSX | ~500 | Task author | — | Unconstrained EURs |

## 5. Deterministic solution path

1. Filter wells; build monthly rate per producing day; drop low-day months; identify peak.
2. Grid-search fits with terminal switch; compute EUR per well.
3. Exceedance percentiles; report the type curve.
4. Contrast with unconstrained and exponential fits.

## 6. Wrong paths (method errors, not misreadings)

**A — no terminal decline.** EUR inflated, P10 explodes.

**B — exponential on early data.** EUR understated.

**C — monthly volumes without producing-day normalization.** Downtime read as decline.

**D — percentile convention reversed.** P90 and P10 swapped.

## 7. Why the stump is analytical, not semantic

The model, grid, normalization and percentile convention are written down. The trap is physical/statistical: an unbounded decline
family and transient data — classic reserve-estimation errors.

## 8. Draft task prompt (prose)

> Publish our Marcellus type curve under the reserves memo: fit each analysis well's modified hyperbolic decline on rate per producing
> day, compute 30-year EURs and give me P90/P50/P10. Provide `well_eurs.csv` (well: fitted q_i, b, D_i, switch month, cumulative, EUR),
> `type_curve.png` (EUR distribution with the three cut-offs and the analyst's unconstrained P50 marked), and a one-page
> `type_curve_memo.pdf`.

## 9. Deliverables

* `well_eurs.csv`, `type_curve.png`, `type_curve_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* P90/P50/P10; fits for 10 spot-check wells (b, D_i, EUR); count of wells with b > 1; unconstrained and exponential contrasts.

## 11. Golden-output checklist

* Producing-day normalization; peak handling; grid search; terminal switch; 30-year horizon; exceedance convention.

## 12. Build notes (scope tuning)

* Limit to a few counties to keep 300–800 wells; publish the reference fit for three wells.
* Confirm the unconstrained P50 exceeds the constrained P50 by > 20%.
