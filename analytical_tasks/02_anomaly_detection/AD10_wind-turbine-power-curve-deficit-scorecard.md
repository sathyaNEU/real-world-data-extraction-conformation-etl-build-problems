# AD10 — Is a wind turbine underperforming? Compare it with its own power curve, not with its neighbours or last year

| Field | Value |
|---|---|
| Category | Anomaly Detection & Diagnostics |
| Domain | Wind energy asset management / operations & maintenance |
| Task shape | 10 · Scorecard against thresholds (turbine × test → inspect / clear) |
| Core method | IEC 61400-12-style method of bins on 10-minute SCADA data with air-density normalization and abnormal-operation filtering; energy deficit computed by applying the baseline curve to the current year's wind distribution |
| Analytical stump | Year-over-year energy differences mostly reflect wind; neighbour comparisons reflect wakes; unfiltered data mix downtime and curtailment into "performance"; seasonal density changes shift power at the same wind speed. Only a normalized, filtered power-curve comparison isolates the turbine |
| Primary sources | Kelmarsh wind farm SCADA and status data (Zenodo, CC BY 4.0) |

## 1. The real-world situation

An asset manager runs a six-turbine wind farm. Year-end reporting showed one turbine produced 7% less energy in 2021 than
in 2017 and 4% less than the farm average, and the O&M contractor was asked to schedule a costly blade inspection. The
performance engineer wanted to know whether the turbine had actually degraded — or whether wind, wakes, curtailment and
outages explained the shortfall.

## 2. The decision (one deterministic recommendation)

**Which turbines, if any, fail the performance test and are sent for inspection?** (Per-turbine go/no-go; the headline is
the inspection list.)

Rules (performance engineering memo):

* Data: 10-minute SCADA for 2017 (baseline) and 2021 (test) per turbine; status/event logs.
* Filters (both years): turbine in normal operation for the full 10 minutes (no stop/warning/curtailment status overlapping
  the interval), power-setpoint at rated (no derating), wind speed 3–20 m/s, no icing flags, data present for wind speed,
  power and nacelle temperature.
* Air-density normalization: ρ = p ÷ (287.05 × T) with T from the ambient temperature channel (K) and p = site standard
  pressure from the memo (altitude-adjusted); V_n = V × (ρ ÷ 1.225)^(1/3).
* Baseline power curve: 2017 filtered data binned by V_n in 0.5 m/s bins (bins with ≥ 10 records), mean power per bin.
* Test: expected 2021 energy = Σ over 2021 filtered records of baseline power at that record's V_n bin (records in bins
  absent from the baseline are dropped from both sums); deficit = 1 − actual ÷ expected.
* Tests per turbine: T1 deficit ≤ 3%; T2 filtered-data coverage ≥ 60% of 2021 intervals; T3 baseline bins cover 4–14 m/s.
  Inspect if T1 fails while T2 and T3 pass.

## 3. Why capable analysts get it wrong

* Annual energy is dominated by the wind resource, which varies several percent year to year.
* Neighbouring turbines sit in each other's wakes for some wind directions; the farm average is not a clean reference.
* Downtime, curtailment and derating appear as low power at high wind; they belong to availability, not performance.
* Cold air is denser; the same wind speed yields more power in winter; density normalization is needed for curve
  comparisons.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–12 | `Turbine_Data_Kelmarsh_<n>_2017-01-03_-_2018-01-01_<id>.csv` and `…2021…csv` (6 turbines × 2 years) | CSV | ~52k rows each, many columns | Kelmarsh wind farm data, Zenodo | CC BY 4.0 | 10-minute SCADA |
| 13–14 | `Status_Kelmarsh_<n>_2017….csv`, `…2021….csv` (per turbine) | CSV | 1k–20k each | Zenodo Kelmarsh | CC BY 4.0 | Stop/warning/curtailment events |
| 15 | `Kelmarsh_WT_static.csv` | CSV | 6 | Zenodo Kelmarsh | CC BY 4.0 | Coordinates, hub height, model |
| 16 | `kelmarsh_readme.pdf` | PDF | — | Zenodo record | CC BY 4.0 | Channel definitions |
| 17 | `iec_61400_12_1_method_summary.pdf` (public summary; cite standard) | PDF | — | Cite | Cite | Method of bins, density normalization |
| 18 | `performance_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 19 | `yearend_energy_report.xlsx` | XLSX | 6 | Task author | — | The raw energy comparison |

## 5. Deterministic solution path

1. Load SCADA and status logs; flag intervals overlapping abnormal statuses; apply all filters.
2. Compute density and normalized wind speed; build 2017 baseline curves per turbine.
3. Compute 2021 expected and actual energy over matched bins; deficits; coverage; bin coverage.
4. Scorecard and inspection list; contrast with raw energy, farm-average and unfiltered comparisons.

## 6. Wrong paths (method errors, not misreadings)

**A — raw energy year-over-year.** Wind-year difference read as degradation.

**B — farm-average comparison.** Wake-affected turbine flagged.

**C — no status filtering.** Downtime/curtailment appear as performance loss.

**D — no density normalization.** Seasonal mix differences shift the curve.

## 7. Why the stump is analytical, not semantic

Channels and statuses are documented; the memo fixes filters, normalization and bins. The traps are confounders (wind
resource, wakes, availability, density) that only a properly normalized comparison removes.

## 8. Draft task prompt (prose)

> Before we pay for blade inspections, test each turbine's 2021 performance against its own 2017 power curve exactly as the
> performance memo describes, and tell me which turbines, if any, need inspection. Use the Kelmarsh SCADA and status files in
> the folder. Provide `performance_scorecard.csv` (turbine: filtered coverage, bin coverage, expected and actual energy,
> deficit, each test, decision) and `power_curves.png` showing each turbine's 2017 and 2021 normalized curves. Add a one-page
> `inspection_memo.pdf` with the list and an explanation of how much of the year-end shortfall was wind, availability and
> real performance.

## 9. Deliverables

* `performance_scorecard.csv`, `power_curves.png`, `inspection_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* 6 turbines × (3 tests + deficit) = 24; inspection list; shortfall attribution for the flagged turbine.

## 11. Golden-output checklist

* Status-overlap filtering; density normalization; per-turbine baseline; matched-bin energy; tests applied.

## 12. Build notes (scope tuning)

* Confirm that the turbine flagged by the year-end report is cleared (or confirmed) by the method and that at least one
  trap reverses the call.
* Copy the exact status-code categories to exclude from the Kelmarsh readme into the memo.
