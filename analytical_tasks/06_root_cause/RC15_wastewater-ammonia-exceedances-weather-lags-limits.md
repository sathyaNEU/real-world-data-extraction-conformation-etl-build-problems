# RC15 — Ammonia permit violations surged this spring: wet weather, cold water, or a tighter seasonal limit?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | KPI breaches where the threshold itself moves (seasonal SLAs, tiered credit limits, quarterly quotas) and process KPIs that respond to drivers with lags |
| Domain | Water utilities / environmental compliance |
| Task shape | 18 · Hypotheses versus evidence (wet-weather inflow, cold-water nitrification loss, seasonal limit step, loading growth → evidence lines from a plant panel; the cause the regulator acts on) |
| Core method | Panel of municipal treatment plants × months from discharge monitoring reports; model the effluent ammonia concentration itself (not the exceedance flag) with plant fixed effects and month-of-year effects, on same-month precipitation, lagged air temperature (1 month, as a wastewater-temperature proxy) and flow ÷ design flow; counterfactual exceedances by swapping each driver to the reference year; separately count exceedances caused purely by limit steps (concentration within the old limit, above the new one) |
| Analytical stump | Exceedance counts depend on both the effluent and the limit. Permits reissued during the year added or tightened spring ammonia limits, so a year-over-year surge in spring exceedances can occur with no change in effluent. Pooled correlations between precipitation and exceedances are confounded by plant type (combined-sewer systems sit in wetter regions), and nitrification responds to temperature with a lag, so a same-month correlation understates it |
| Primary sources | U.S. EPA ECHO / ICIS-NPDES discharge monitoring report (DMR) data and permit limits; NOAA nClimDiv monthly climate division precipitation and temperature |

## 1. The real-world situation

A state water-quality regulator saw ammonia-nitrogen exceedances at municipal plants in March–May jump to roughly twice the previous year's count.
The utility association blamed an exceptionally wet spring (inflow and infiltration washing out the biomass). Regulators drafting an enforcement
initiative needed to know which explanation the evidence supports before choosing between I/I enforcement, nitrification upgrades, or no
plant-level action.

## 2. The decision (one deterministic recommendation)

**The explanation the regulator acts on — the hypothesis with the largest attributable share of the excess exceedances — with the evidence grid.**

Rules (compliance memo):

* Plants: major municipal POTWs in the state with monthly ammonia (as N) DMR values for the reference and current years and a monthly average limit.
* Concentration: monthly average ammonia (mg/L) per plant-month; flow ratio = monthly average flow ÷ design flow.
* Weather: nClimDiv precipitation (same month) and average temperature lagged 1 month for each plant's climate division.
* Model, fitted on 5 years before the current year: log(ammonia + 0.1) = plant FE + month-of-year FE + β1·precip + β2·temp(lag 1) + β3·flow ratio.
* Exceedance = concentration > the limit in force that month.
* Attribution of excess exceedances (current spring − reference spring):
  * Limit step: plant-months exceeding the current limit but within the limit in force in the same month of the reference year.
  * Each driver: predicted exceedances with that driver at its observed current value minus predicted with it at its reference-year value (others
    observed), using the model's residual distribution for probabilities; shares normalised to the excess not explained by limit steps.
  * Loading growth = the flow-ratio share.
* Evidence lines per hypothesis: sign and significance of the coefficient (p < 0.05), attributable share, and timing (precipitation same month,
  temperature at lag 1).
* Act on the hypothesis with the largest attributable share.

## 3. Why capable analysts get it wrong

* "Exceedances" are counted as if the limit were fixed, but reissued permits changed it between the two springs.
* Wet springs and violations co-occur, and wetter regions host older combined systems.
* Biological processes respond to temperature with a delay.
* Flags discard the continuous concentration information needed for attribution.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `npdes_dmrs_<state>_<years>.csv` | CSV | ~400k parameter-months | EPA ECHO DMR downloads (ICIS-NPDES) | U.S. Government work (public domain) | Effluent values and flows |
| 2 | `npdes_limits_<state>.csv` | CSV | ~60k | EPA ICIS-NPDES limits | Public domain | Monthly and seasonal limits |
| 3 | `npdes_facilities_<state>.csv` | CSV | ~2k | EPA ECHO facility data | Public domain | Facility type, design flow, coordinates |
| 4 | `nclimdiv_pcp_tmp.txt` | TXT (fixed width) | ~350k | NOAA NCEI nClimDiv | Public domain | Monthly climate-division weather |
| 5 | `climdiv_boundaries.geojson` | GeoJSON | ~350 | NOAA NCEI | Public domain | Plant → division mapping |
| 6 | `compliance_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 7 | `association_wet_weather_letter.pdf` | PDF | — | Task author | — | The I/I explanation |

## 5. Deterministic solution path

1. Select plants and ammonia parameters; harmonise units; attach limits by month; flag exceedances.
2. Map plants to climate divisions; join weather; build the panel.
3. Fit the fixed-effects model on the 5 prior years; residual distribution.
4. Count limit-step exceedances; attribute the remainder by driver swaps.
5. Evidence grid and decision; contrast with the association's letter.

## 6. Wrong paths (method errors, not misreadings)

**A — exceedance counts with a fixed limit assumption.** Limit-step violations attributed to plant performance.

**B — pooled cross-plant correlation of precipitation and exceedances.** Confounded by plant type and region.

**C — same-month temperature.** Misses the lag and understates the cold-water effect.

**D — logistic model on exceedance flags.** Discards concentration information; unstable with rare events.

## 7. Why the stump is analytical, not semantic

Limits and DMR values are numeric fields; the model, lags and attribution are specified. The trap is a moving threshold and lagged, confounded
drivers.

## 8. Draft task prompt (prose)

> Spring ammonia violations doubled and the utilities say it was the wet weather. Use the compliance memo's panel model and attribution to tell me
> what actually drove the increase and which action we should take. Provide `exceedance_attribution.csv` (component: exceedances, share),
> `evidence_grid.png`, and a one-page `ammonia_rca.pdf`.

## 9. Deliverables

* `exceedance_attribution.csv` — limit step, precipitation, temperature, loading, unexplained.
* `evidence_grid.png` — hypotheses × evidence lines with consistent/inconsistent marks.
* `ammonia_rca.pdf` — decision, coefficients, timing evidence, and the contrast with the association's explanation.

## 10. Where 25+ rubric criteria come from

* Panel construction (plants, plant-months, unit harmonisation, limit attachment): 5.
* Coefficients β1–β3 with significance: 6.
* Limit-step exceedance count: 2.
* Attributable exceedances and shares by driver: 8.
* Decision and association contrast: 3.
* Grid elements: 3+.

## 11. Golden-output checklist

* Limit in force by month, including seasonal steps.
* 1-month temperature lag; plant and month-of-year fixed effects; 5-year fit window.
* Limit-step count separated before driver attribution.
* Shares normalised as specified.

## 12. Build notes (scope tuning)

* Choose a state where a batch of permits was reissued with tighter spring ammonia limits between the reference and current years, and the current
  spring was wetter than normal; confirm that the limit step plus the temperature effect exceed the precipitation share.
