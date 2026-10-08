# RC08 — A wind turbine producing 6% less: yaw error, pitch fault or ice? Each leaves a different signature

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Equipment underperformance diagnosis at OEMs and operators (GE, Siemens, Vestas service teams) and any asset where several faults reduce the same output |
| Domain | Wind energy operations |
| Task shape | 18 · Hypotheses versus evidence (yaw misalignment, pitch offset, blade icing, curtailment → evidence lines; the fault dispatched to the service team) |
| Core method | Normalised power-curve residuals (actual − reference power at the same air-density-corrected wind speed) by condition bins: residual vs nacelle–wind direction offset (yaw), residual vs pitch angle at rated wind (pitch), residual vs temperature/humidity near freezing (icing), flagged curtailment setpoints; evaluate evidence lines per hypothesis |
| Analytical stump | Total energy shortfall versus the fleet does not identify the fault; each cause has a distinct conditional pattern (yaw losses grow with misalignment across wind speeds; pitch offsets show at rated power; icing appears only near 0 °C with high humidity). Conditioning on the right variables separates them |
| Primary sources | ENGIE La Haute Borne wind farm open data (10-minute SCADA for 4 turbines) |

## 1. The real-world situation

A wind-farm operator saw one turbine producing about 6% less than its neighbours over a winter. The service contractor proposed replacing the
pitch bearing. The asset manager wants the evidence for each candidate fault before dispatching a crew.

## 2. The decision (one deterministic recommendation)

**The fault dispatched (the hypothesis whose evidence lines are all consistent), with the estimated energy loss attributable to it.**

Rules (asset memo):

* Data: La Haute Borne 10-minute SCADA for the turbine and its neighbours (variables: active power, wind speed, wind direction, nacelle angle, pitch
  angle, outdoor temperature, and others per dataset).
* Reference power curve: neighbours' binned power curve (0.5 m/s bins) in the same period, air-density corrected.
* Residual = actual − reference at the turbine's wind speed.
* Evidence: (yaw) |residual| increases with |wind direction − nacelle angle| offset, slope significant (p < 0.01) across 5–12 m/s; (pitch) at wind
  ≥ rated, mean pitch angle differs from neighbours by > 1° and residual negative; (icing) residuals concentrated (≥ 70% of loss) in periods with
  temperature −3 to +2 °C; (curtailment) power capped at a setpoint (flat-top) in ≥ 10% of rated-wind periods.
* Dispatch: hypothesis with all its evidence consistent; energy loss = Σ negative residuals in periods matching that hypothesis's condition.

## 3. Why capable analysts get it wrong

* Monthly energy comparisons don't show mechanisms.
* Several faults reduce output; their signatures overlap without conditioning.
* Air density and neighbours' curves are needed for a fair reference.
* Icing is seasonal and confounds winter comparisons.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `la-haute-borne-data-2017-2020.csv` | CSV | ~840k (4 turbines × 10-min) | ENGIE open data (La Haute Borne) | Licence Ouverte / Etalab 2.0 | SCADA |
| 2 | `data_description.csv` | CSV | ~140 variables | ENGIE | Licence Ouverte | Variable definitions |
| 3 | `static_information.csv` | CSV | 4 | ENGIE | Licence Ouverte | Turbine specs |
| 4 | `asset_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 5 | `contractor_proposal.xlsx` | XLSX | — | Task author | — | Pitch hypothesis |
| 6 | `iec_61400_12_density_correction_citation.pdf` | PDF | — | Cite | Cite | Normalisation |

## 5. Deterministic solution path

1. Filter periods; density-correct wind speed; neighbours' reference curve.
2. Residuals; evidence tests per hypothesis.
3. Dispatch; energy loss; contrast with contractor's proposal.

## 6. Wrong paths (method errors, not misreadings)

**A — monthly energy comparison.** No mechanism.

**B — manufacturer's warranted curve as reference.** Site effects confound.

**C — ignoring temperature conditions.** Icing misattributed.

**D — pooling all wind speeds for pitch test.** Signal diluted.

## 7. Why the stump is analytical, not semantic

The evidence tests are specified. The trap is diagnosing from totals instead of conditional signatures.

## 8. Draft task prompt (prose)

> Which fault explains turbine 3's shortfall? Evaluate the yaw, pitch, icing and curtailment evidence in the asset memo and estimate the attributable
> loss. Provide `fault_evidence_grid.csv` (hypothesis × evidence: statistic, consistent?), `residual_signatures.png`, and a one-page `dispatch_decision.pdf`.

## 9. Deliverables

* `fault_evidence_grid.csv`, `residual_signatures.png`, `dispatch_decision.pdf`.

## 10. Where 25+ rubric criteria come from

* 4 hypotheses × evidence lines (≈ 10 cells); slopes, offsets, shares; energy loss; dispatch; contractor contrast.

## 11. Golden-output checklist

* Density correction; reference curve; residuals; tests; dispatch rule.

## 12. Build notes (scope tuning)

* Choose a turbine-period with a documented or visible nacelle offset; confirm pitch evidence is inconsistent.
