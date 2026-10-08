# DS32 — Choosing wind sites for a supply portfolio: the three best sites can all go quiet together

| Field | Value |
|---|---|
| Category | Decision Support |
| Mirrors | Diversification decisions (multi-region suppliers, multi-cloud deployments, data-centre siting) where correlated failures or shortfalls matter more than individual averages |
| Domain | Renewable energy procurement |
| Task shape | 01 · Ranked list under a cap (3 sites chosen from 10 for a corporate power-purchase portfolio, maximising the portfolio's 10th-percentile hourly output in winter evenings) |
| Core method | Hourly capacity-factor time series per site; portfolio output = mean of selected sites' capacity factors; evaluate the P10 of portfolio output over the memo's critical hours across 7 years; exhaustive search over 120 three-site combinations; compare with picking the three highest mean capacity factors |
| Analytical stump | The three sites with the highest average capacity factor tend to share weather (same region), so their lulls coincide; the portfolio's low-output hours are not improved. Diversification depends on correlation in the tail, not on averages |
| Primary sources | NREL WIND Toolkit (hourly wind speeds/power at 100 m for site locations) |

## 1. The real-world situation

A data-centre operator buys wind power through PPAs and needs supply during winter evening peaks. The procurement team shortlisted 10 sites and
proposed the three with the highest average capacity factor, all in the same plains region. The risk team asked how the portfolio performs in the
hours that matter.

## 2. The decision (one deterministic recommendation)

**The 3-site portfolio maximising P10 of hourly portfolio capacity factor during winter evenings (Dec–Feb, 17:00–21:00 local) over 7 years, and the
same statistic for the procurement team's portfolio.**

Rules (procurement memo):

* Data: WIND Toolkit hourly power (or wind speed converted with the memo's power curve) for 10 site coordinates, 2007–2013.
* Critical hours: Dec–Feb, 17:00–21:00 local time.
* Portfolio CF_t = mean of the three sites' CF_t (equal capacity).
* Objective: P10 of portfolio CF_t over critical hours; exhaustive search (120 combinations); ties → higher mean CF.
* Report mean CF and correlation matrix for context.

## 3. Why capable analysts get it wrong

* Average capacity factor is the headline site metric.
* Correlated weather makes same-region sites redundant in low-wind hours.
* The objective is a tail statistic over specific hours.
* Exhaustive search is cheap for 120 combinations.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–10 | `wtk_site_<id>_2007_2013.csv` (10 sites) | CSV | ~61k hours each | NREL WIND Toolkit (via HSDS/API) | CC BY 4.0 (NREL data) | Hourly wind/power |
| 11 | `site_list.json` | JSON | 10 | Task author | — | Coordinates, regions |
| 12 | `power_curve.json` | JSON | — | Task author (generic IEC class turbine) | — | Conversion |
| 13 | `procurement_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 14 | `procurement_shortlist.xlsx` | XLSX | 10 | Task author | — | Naive choice |
| 15 | `wind_toolkit_documentation.pdf` | PDF | — | NREL (cite) | CC BY 4.0 | Data description |

## 5. Deterministic solution path

1. Load series; convert to CF; local time; critical hours.
2. Evaluate 120 combinations; P10; choose.
3. Contrast with top-3 mean CF portfolio; correlations.

## 6. Wrong paths (method errors, not misreadings)

**A — top-3 by mean CF.** Correlated lulls.

**B — objective over all hours.** Not the memo's critical window.

**C — UTC hours.** Window misaligned.

**D — greedy selection.** May miss the best combination.

## 7. Why the stump is analytical, not semantic

The objective and search are specified. The trap is ignoring correlation when combining assets.

## 8. Draft task prompt (prose)

> Which three wind sites give the most reliable winter-evening supply? Evaluate all combinations by the portfolio P10 in critical hours as the procurement
> memo specifies. Provide `portfolio_grid.csv` (combination: P10, mean CF), `site_correlation.png`, and a one-page `ppa_portfolio.pdf`.

## 9. Deliverables

* `portfolio_grid.csv`, `site_correlation.png`, `ppa_portfolio.pdf`.

## 10. Where 25+ rubric criteria come from

* Chosen combination; its P10 and mean; top 10 combinations' P10; procurement portfolio P10; correlations for 10 site pairs.

## 11. Golden-output checklist

* Conversion; local time; window; exhaustive search; ties.

## 12. Build notes (scope tuning)

* Choose sites in 3–4 regions; confirm the procurement portfolio ranks outside the top 20 combinations by P10.
