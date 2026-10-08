# FC23 — How much solar energy can we sell forward? A one-year P90 is not a ten-year P90

| Field | Value |
|---|---|
| Category | Forecasting & Predictive Modelling |
| Mirrors | Renewable-energy procurement and project finance (corporate PPAs, forward hedges, debt sizing on P50/P90 energy) |
| Domain | Solar asset management / energy trading |
| Task shape | 14 · Cuts of a distribution (P50/P75/P90/P99 annual energy for 1-year and 10-year horizons) |
| Core method | Long irradiance record converted to energy with a performance ratio calibrated on measured production; interannual variability measured on annual totals; exceedance levels for single years vs multi-year averages; degradation |
| Analytical stump | Interannual variability must be measured on annual sums; scaling monthly variability by √12 assumes independent months with equal variance. A one-year hedge needs the single-year exceedance; the ten-year P90 (σ ÷ √10) is far tighter and oversells. Forgetting degradation overstates later years |
| Primary sources | NREL PVDAQ measured PV system data, NREL NSRDB multi-year irradiance |

## 1. The real-world situation

A corporate buyer's energy desk wants to sell forward the output of an owned solar plant for **2027**, choosing a volume it is
90% confident the plant will meet in that year. The analyst used the lender's P90 from the financing model — a ten-year P90 — and
scaled monthly irradiance variability by √12. The volume looked comfortably safe; the risk team disagreed.

## 2. The decision (one deterministic recommendation)

**The 2027 forward volume = the one-year P90 of 2027 energy (MWh), with the full exceedance table.**

Rules (energy-desk memo):

* Plant: the PVDAQ system in the folder (DC/AC ratings in metadata). Measured AC energy 2015–2023 calibrates a performance ratio
  PR = Σ measured energy ÷ Σ (rated DC kW × plane-of-array insolation in kWh/m² ÷ 1 kW/m²) using NSRDB-derived POA insolation for
  the same days (days with > 5% missing measurements excluded from both sums).
* Long-term record: NSRDB annual POA insolation 1998–2022 for the site (25 years), computed with the transposition settings in the
  memo.
* Energy in a weather year y for 2027 = rated DC × POA_y × PR × (1 − 0.005)^(2027 − 2023).
* One-year exceedance: P_x = mean − z_x × σ, with mean and σ (sample SD) of the 25 annual energies, z from the normal
  distribution. Ten-year: σ ÷ √10.
* Forward volume = one-year P90, rounded down to the nearest 10 MWh.

## 3. Why capable analysts get it wrong

* Financing models report ten-year P90s (appropriate for average debt service capacity), not single-year values.
* Monthly variability scaled by √12 ignores seasonal heteroscedasticity and correlation between months.
* Measured production includes outages; calibrating PR without excluding gaps biases it.
* Degradation is small per year but compounds.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1–9 | `pvdaq_system_<id>_YYYY.csv` (2015–2023) | CSV | ~100k–500k each (1–5 min data) | NREL PVDAQ (OEDI) | Public (NREL data terms) | Measured AC power |
| 10 | `pvdaq_system_<id>_metadata.json` | JSON | 1 | NREL PVDAQ | Public | Ratings, tilt, azimuth |
| 11 | `nsrdb_psm_<site>_1998_2022.csv` | CSV | ~220k hourly | NREL NSRDB | NREL data terms (attribution) | GHI, DNI, DHI |
| 12 | `poa_daily_<site>_1998_2023.parquet` | Parquet | ~9k | Derived (transposition per memo) | Same | POA insolation |
| 13 | `pvdaq_data_quality_notes.pdf` | PDF | — | NREL | Public | Gaps, sensor notes |
| 14 | `energy_desk_memo.pdf` | PDF | — | Task author | — | Rules in §2 |
| 15 | `lender_p90_summary.xlsx` | XLSX | ~10 | Task author | — | Ten-year P90 figure |

## 5. Deterministic solution path

1. Clean measured data; daily energy; exclude incomplete days; compute PR against POA insolation.
2. Compute annual POA for 1998–2022; annual 2027 energy with degradation.
3. Mean and σ of the 25 annual energies; one-year and ten-year exceedance table; forward volume.
4. Contrast with monthly-√12 and ten-year approaches.

## 6. Wrong paths (method errors, not misreadings)

**A — ten-year P90 for a one-year hedge.** Volume too high; shortfall risk ≫ 10%.

**B — monthly σ × √12.** Mis-states annual σ.

**C — PR from unfiltered data.** Outages lower PR; volume too low.

**D — no degradation.** Volume overstated.

## 7. Why the stump is analytical, not semantic

The memo defines PR, the record and exceedance formulas. The traps concern variance aggregation over time and the horizon of a
quantile — statistical reasoning, not field interpretation.

## 8. Draft task prompt (prose)

> We want to sell forward the 2027 output of our solar plant at a volume we are 90% confident of producing that year, following the
> energy-desk memo. Calibrate the plant on its measured data, run 25 weather years and give me the forward volume. Provide
> `exceedance_table.csv` (P50/P75/P90/P99 for one-year and ten-year horizons, mean, σ, PR), `annual_energy_distribution.png` with the
> 25 annual energies and both P90s marked, and a one-page `hedge_memo.pdf` with the volume and the shortfall probability of the
> lender's figure.

## 9. Deliverables

* `exceedance_table.csv`, `annual_energy_distribution.png`, `hedge_memo.pdf`.

## 10. Where 25+ rubric criteria come from

* PR; 25 annual energies (spot-check 8); mean, σ; 8 exceedance values; volume; lender-figure shortfall probability.

## 11. Golden-output checklist

* Gap-filtered PR; annual-sum σ; one-year P90; degradation; rounding.

## 12. Build notes (scope tuning)

* Pick a PVDAQ system with ≥ 8 years of good data and a nearby NSRDB grid cell; document the transposition model settings.
* Confirm the ten-year P90 exceeds the one-year P90 by > 5%.
